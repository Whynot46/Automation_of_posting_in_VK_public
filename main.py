import vk_api
import requests
import time
import json
token = 'vk1.a.vpBPh4jTyEBeOATnvSQqCoGfnlJKU_zunR8WGrotvTb4Ds2Onf6Dva-KfCjUfCSp6DaD94rllPHPzJ7mXKi31V3MZw3O9lTMbZ1XbscoPXoYM4pFQ0jDm7XQ9EHHNESlYqnXgJu2C6mFYd9mw9ri9T33Aw3-wv-IV5SMXX1pf3mHkd62UIrphfw51jf42IWogFBq3nDVjiPZD0i7_SyzAw'
owner_id = -144688488
from_group = 1
version_vk = '5.131'
url = 'https://api.vk.com/method/wall.post'

try:
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
except Exception as e:
    print(f'Ошибка при создании сессии vk_api: {e}')
    exit()

tools = vk_api.VkTools(vk_session)

source_group_ids = [-145945161, -219611209]

start_time = time.time()

start_from = None


while True:

    print(f'Начало парсинга: {start_time}')

    for source_group_id in source_group_ids:
        current_time = time.time()
        end_date = current_time + 10

        try:
            wall = tools.get_all('wall.get', 10, {'owner_id': int(source_group_id), 'start_time': int(start_time),
                                                  'end_time': int(current_time), 'start_from': start_from})
        except Exception as e:
            print(f'Ошибка при получении постов из группы {source_group_id}: {e}')
            continue

        for post in wall['items']:

            if post['date'] >= start_time:

                message = post['text'] or ' '

                attachments = ''
                if 'attachments' in post:
                    for attachment in post['attachments']:
                        if attachment['type'] == 'photo':
                            try:

                                upload_url = vk.photos.getWallUploadServer(group_id=-owner_id, v=version_vk)[
                                    'upload_url']
                                print(upload_url)
                                photo_url = attachment['photo']['sizes'][-1]['url']
                                
                                print(photo_url)

                                photo_data = requests.post(upload_url, files={
                                    'photo': ('photo.jpg', requests.get(photo_url).content)
                                }).json()
                                print(photo_data['photo'])

                                photo = vk.photos.saveWallPhoto(group_id=-owner_id, photo=photo_data['photo'],
                                                                server=photo_data['server'], hash=photo_data['hash'],
                                                                v=version_vk)[0]

                                attachments += f'photo{photo["owner_id"]}_{photo["id"]}_{photo["access_key"]},'
                            except Exception as e:
                                print(f'Ошибка при копировании фото: {e}')
                        elif attachment['type'] == 'video':
                            try:

                                name = attachment['video']['title']

                                if 'platform' in attachment['video']:

                                    if attachment['video']['platform'] == 'VK':

                                        attachments += f'video{attachment["video"]["owner_id"]}_{attachment["video"]["id"]}_{attachment["video"]["access_key"]},'
                                    else:

                                        upload_url = vk.video.save(group_id=-owner_id, is_private=1, wallpost=0,
                                                                   player=attachment['video']['player'], name=name,
                                                                   v=version_vk)[
                                            'upload_url']
                                        print(upload_url)

                                        video_data = requests.post(upload_url).json()

                                        video = vk.video.save(group_id=-owner_id, video_id=video_data['video_id'],
                                                              v=version_vk)

                                        attachments += f'video{video["owner_id"]}_{video["id"]}_{video["access_key"]},'
                                else:

                                    attachments += f'video{attachment["video"]["owner_id"]}_{attachment["video"]["id"]}_{attachment["video"]["access_key"]},'
                            except Exception as e:
                                print(f'Ошибка при копировании видео: {e}')
                        elif attachment['type'] == 'poll':
                            try:

                                poll_data = attachment['poll']
                                poll_question = poll_data['question']
                                poll_answers = [answer['text'] for answer in poll_data['answers']]
                                poll_anonymous = poll_data.get('anonymous', 0)
                                poll_multiple = poll_data.get('multiple', 0)
                                poll_end_date = poll_data.get('end_date', end_date)
                                poll_is_closed = poll_data.get('is_closed',
                                                               0)  # получаем значение параметра is_closed из исходного опроса

                                poll_answers_json = json.dumps(poll_answers)

                                poll = vk.polls.create(question=poll_question,
                                                       add_answers=poll_answers_json,
                                                       is_anonymous=poll_anonymous,
                                                       multiple=poll_multiple,
                                                       end_date=end_date,
                                                       is_closed=poll_is_closed,
                                                       # передаем то же значение параметра is_closed при создании нового опроса
                                                       owner_id=-owner_id,
                                                       v=version_vk)

                                attachments += f'poll{poll["owner_id"]}_{poll["id"]},'
                            except Exception as e:
                                print(f'Ошибка при копировании опроса: {e}')
                        elif attachment['type'] == 'doc':
                            try:

                                doc_data = attachment['doc']
                                doc_title = doc_data['title']
                                doc_ext = doc_data['ext']
                                doc_url = doc_data['url']

                                upload_url = vk.docs.getWallUploadServer(group_id=-owner_id,
                                                                         v=version_vk)['upload_url']
                                print(upload_url)

                                doc_file = requests.post(upload_url, files={
                                    'file': (f'{doc_title}.{doc_ext}', requests.get(doc_url).content)
                                }).json()['file']

                                doc = vk.docs.save(file=doc_file,
                                                   title=doc_title,
                                                   v=version_vk)['doc']

                                attachments += f'doc{doc["owner_id"]}_{doc["id"]}_{doc["access_key"]},'
                            except Exception as e:
                                print(f'Ошибка при копировании документа: {e}')
                try:
                    response = requests.post(
                        url=url,
                        params={
                            'access_token': token,
                            'from_group': from_group,
                            'owner_id': owner_id,
                            'message': message,
                            'attachments': attachments.strip(','),
                            'v': version_vk,
                        }
                    )
                except Exception as e:
                    print(f'Ошибка при публикации поста: {e}')
                else:

                    print(response.json())

                time.sleep(1)

        if 'next_from' in wall:
            start_from = wall['next_from']
        else:
            start_from = None

    start_time = current_time
    print(f'Конец парсинга: {current_time}')

    time.sleep(20)