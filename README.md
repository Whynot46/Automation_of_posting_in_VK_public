[![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%7006BCF9&lines=Automation_of_posting_in_VK_public)](https://git.io/typing-svg)
<p>Script for automatic parsing of VK publics and publishing identical posts to the parent public.</p>
<p>Especially for the department of education, sports and youth policy of the municipality "Privolzhsky district" of the Astrakhan region.</p>
<hr>
<p>@Developed by Kisilev Dmitry and Pahalev Aleksey</p>
<hr>

<h1>Автоматизация постинга в паблике ВКонтакте</h1>
<p>Скрипт для автоматического парсинга пабликов ВК и публикации идентичных постов в родительском паблике.
<br>
Скрипт парсит список указанных пабликов ВКонтакте и при обнаружении новых публикаций, публикует в родительском паблике точно такой же пост, с точно таким же текстом и прикрепленными файлами,
<br>
добавляя в начале строку "Источник: <Имя_паблика_источника>".</p>
<p>Разработано специально для управления образования, спорта и молодежной политики муниципального образования «Приволжский район» Астраханской области.</p>
<hr>
<p>@Разработано Кисилевым Дмитрием и Пахалевым Алексеем</p>
<hr>
<h2>Инструкция по применению</h2>
<p>1) Первоначально, вам необходимо создать приложение ВКонтакте, сделать это можно этой <a href="https://vk.com/editapp?act=create">ссылке</a>.<br>
2) Укажите название и тип вашего приложения.<br>
3) Выберите платформу Standalone, ибо тогда можно будет получить токен с большим возможностями, чем в остальных вариантах.<br>
<img src="https://badtry.net/content/images/2018/05/create_app.jpg"><br>
4) Создав приложение и перейдя на вкладку настроек, будут показаны id приложения и его секретный ключ.<br>
<img src="https://badtry.net/content/images/2018/05/vk-api-config.jpg"><br>
5) Теперь, имея id приложения, можно получить токен доступа. Для этого нужно сформировать ссылку, подставив в неё id своего приложения.<br>
https://oauth.vk.com/authorize?client_id={CLIENT_ID}&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,notify,photos,wall,email,mail,groups,stats,offline&response_type=token&v=5.74 <br>
где вместо {CLIENT_ID} нужно вставить id своего приложения, а в параметре scope - перечислены разрешения, которыми мы хотим наделить токен, <a href="https://vk.com/dev/permissions">список всех разрешений</a>.<br>
Однако здесь, одним из самых важных разрешений является offline, которое создаёт бессрочный токен, не имеющий ограниченного времени жизни.<br>
6) Перейдя по сформированной ссылке, откроется диалоговое окно, в котором будут показаны разрешения, которыми наделяется токен (чем больше указано scope свойств, тем больше будет этот список).<br>
<img src="https://badtry.net/content/images/2018/05/auth.jpg"><br>
7) Подтвердив, произойдёт переадресация на страницу, в адресной строке которой будет access_token, expires_in равный нулю (что логично, учитывая, что мы указывали создание вечного токена).<br>
<img src="https://badtry.net/content/images/2018/05/token.jpg"><br>
8) Скопируйте полученный access_token и вставьте в файл authorization_data.py, в строчку token = "", внутри кавычек.<br>
9) В файле authorization_data.py, в строке owner_id = "", вставьте внутри кавычек id паблика, в котором будут публиковаться посты.<br>
10) В файле authorization_data.py, в строке source_group_ids = "", вставьте через запятую, внутри кавычек id пабликов, которые вы хотите проверять на наличие новых постов.<br>
11) Сохраните файл authorization_data.py.<br>
12) Если у вас не установлен Python, запустите файл install_python.bat<br>
13) Запустите файл install_libraries.bat, чтобы установить необходимые библиотеки.<br>
14) Настройка окончена, запустите файл start.bat и вы прекрасны!
</p>
