languages = {
    "en": "🇬🇧 English",
    "ru": "🇷🇺 Русский",
    "sr": "🇷🇸 Srpski",
    "geo": "🇬🇪 ქართული",
}

prompt_languages = {
    "en": "English",
    "ru": "Russian",
    "sr": "Serbian latin",
    "geo": "Georgian",
}

commands = {
    "list": {
        "en": "Show all your subscriptions",
        "ru": "Показать все ваши подписки",
        "sr": "Prikaži sve vaše pretplate",
        "geo": "ყველა გამოწერილის ჩვენება",
    },
    "settings": {
        "en": "Change post appearance or change language",
        "ru": "Изменить внешний вид постов или изменить язык",
        "sr": "Promeniti izgled postova ili promeniti jezik",
        "geo": "პოსტის გამოსახულების ან ენის შეცვლა",
    },
}

translations = {
    "en": {
        "go_back": "Go back",
        "select_language": "Select language",
        "select_language_prompt": "Select language",
        "welcome": (
            "🔘 Welcome to Matte!\n\n"
            "Start by providing me any links to RSS feeds. "
            "Go ahead and just send me a message with link (one at a time)."
        ),
        "invalid_url": "Please provide a valid URL to an RSS feed",
        "invalid_feed": "Target resource is not a valid feed",
        "unable_to_get_feed": "I'm currently unable to get a feed from this source, please try again later",
        "summarization_unavailable": "Summarization is unavailable for this post",
        "subscribed": "Successfully subscribed to",
        "unsubscribed": "Successfully unsubscribed from a feed!",
        "last_update": "Last update in this feed:",
        "no_last_update": (
            "There are no recent updates in this feed at the moment, but I'll send you any once they appear!"
        ),
        "settings_list": "Here's the list of settings:",
        "sample_post_preview": "Posts will appear like this:",

        "settings": {
            "feed_name": "Display a feed title",
            "post_name": "Display a post title",
            "post_link_in_post_name": "Embed a post link into post name",
            "show_preview": "Show page preview",
        },
        "summarize_post": "Summarize post",
        "summary": "Summary",
        "no_subscriptions": "You have no subscriptions at the moment. Send me a link to subscribe to a feed!",
        "your_subscriptions": "Your subscriptions",
        "unsubscribe_prompt": "Send the link again to unsubscribe from a feed.",
        "setting_enabled": "Enabled",
        "setting_disabled": "Disabled",
    },
    "ru": {
        "go_back": "Назад",
        "select_language": "Выбрать язык",
        "select_language_prompt": "Выберите язык",
        "welcome": (
            "🔘 Добро пожаловать в Matte!\n\n"
            "Пришлите мне ссылки на RSS-фиды в форматах RSS или Atom "
            "(по одной за раз), и я начну присылать вам обновления."
        ),
        "invalid_url": "Пожалуйста, пришлите корректный URL RSS-фида",
        "invalid_feed": "Ресурс не является фидом",
        "unable_to_get_feed": (
            "В данный момент я не могу получить фид из этого ресурса. Пожалуйста, попробуйте ещё раз позже."
        ),
        "summarization_unavailable": "Обобщение недоступно для этого поста",
        "subscribed": "Вы успешно подписались на",
        "unsubscribed": "Вы успешно отписались от фида!",
        "last_update": "Последнее обновление в этом фиде:",
        "no_last_update": (
            "Пока что в этом фиде нет недавних обновлений, но я пришлю их вам, как только они появятся!"
        ),
        "settings_list": "Список настроек:",
        "sample_post_preview": "Посты будут показываться так:",

        "settings": {
            "feed_name": "Показывать заголовок фида",
            "post_name": "Показывать заголовок поста",
            "post_link_in_post_name": "Включить ссылку на пост в заголовок поста",
            "show_preview": "Показывать предпросмотр поста",
        },
        "summarize_post": "Обобщить пост",
        "summary": "Краткое содержание",
        "no_subscriptions": "Пока что у вас нет подписок. Пришлите мне ссылку чтобы подписаться на фид!",
        "your_subscriptions": "Ваши подписки",
        "unsubscribe_prompt": "Пришлите ссылку снова чтобы отписаться от фида.",
        "setting_enabled": "Включено",
        "setting_disabled": "Отключено",
    },
    "sr": {
        "go_back": "Vrati se",
        "select_language": "Izaberete jezik",
        "select_language_prompt": "Izaberite jezik",
        "welcome": (
            "🔘 Dobrodošli u Matte!\n\n"
            "Počnite tako što ćete mi pružiti bilo koje linkove ka RSS ili Atom feedovima. "
            "Napred i samo mi pošaljite poruku sa linkom (jedan po jedan)."
        ),
        "invalid_url": "Molimo vas da pružite važeći URL ka RSS feedu",
        "invalid_feed": "Ciljani resurs nije važeći feed",
        "unable_to_get_feed": (
            "Trenutno nisam u mogućnosti da dobijem feed iz ovog izvora, molimo pokušajte ponovo kasnije."
        ),
        "summarization_unavailable": "Sažetak nije dostupan za ovaj post",
        "subscribed": "Uspešno pretplaćeni na",
        "unsubscribed": "Uspešno odjavljeni sa feeda!",
        "last_update": "Poslednje ažuriranje u ovom feedu:",
        "no_last_update": (
            "Trenutno nema nedavnih ažuriranja u ovom feedu, ali ću vam poslati čim se pojave!"
        ),
        "settings_list": "Evo liste podešavanja:",
        "sample_post_preview": "Postovi će se pojaviti ovako:",

        "settings": {
            "feed_name": "Prikaži naslov feeda",
            "post_name": "Prikaži naslov posta",
            "post_link_in_post_name": "Ugradi link posta u ime posta",
            "show_preview": "Prikaži pregled stranice",
        },
        "summarize_post": "Sažmi post",
        "summary": "Sažetak",
        "no_subscriptions": "Trenutno nemate pretplate. Pošaljite mi link da se pretplatite na feed!",
        "your_subscriptions": "Vaše pretplate",
        "unsubscribe_prompt": "Pošaljite link ponovo da se odjavite sa feeda.",
        "setting_enabled": "Uključeno",
        "setting_disabled": "Isključeno",
    },
    "geo": {
        "go_back": "უკან დაბრუნება",
        "select_language": "ენის არჩევა",
        "select_language_prompt": "აირჩიეთ ენა",
        "welcome": (
            "🔘 მოგესალმებათ Matte!\n\n"
            "მომაწოდეთ ნებისმიერი RSS ფიდის ბმული. "
            "უბრალოდ გამომიგზავნეთ ბმულის შემცველი მესიჯი (სათითაოდ)."
        ),
        "invalid_url": "გთხოვთ, გამომიგზავნეთ RSS ფიდის ვალიდური ბმული",
        "invalid_feed": "აღნიშნული არ შეესაბამება ვალიდურ ფიდს",
        "unable_to_get_feed": "ამ მომენტში არ შემიძლია აღნიშნული ბმულიდან ფიდის მიღება, მოგვიანებით სცადეთ",
        "summarization_unavailable": "აღნიშნული პოსტის შეჯამება შეუძლებელია",
        "subscribed": "წარმატებით გამოიწერა",
        "unsubscribed": "ფიდის გამოწერა გაუქმდა წარმატებით!",
        "last_update": "აღნიშნული ფიდის ბოლო განახლება:",
        "no_last_update": (
            "აღნიშნული ფიდი ბოლოს დროს არ განახლებულა, მაგრამ როგორც კი განახლდება, გამოგიგზავნით!"
        ),
        "settings_list": "პარამეტრების სია:",
        "sample_post_preview": "პოსტები ასე გამოჩნდება:",

        "settings": {
            "feed_name": "ფიდის სახელის ჩვენება",
            "post_name": "პოსტის სათაურის ჩვენება",
            "post_link_in_post_name": "დაურთე ბმული პოსტის სათაურს",
            "show_preview": "გვერდის წინასწარი ვერსიის ჩვენება",
        },
        "summarize_post": "პოსტის შეჯამება",
        "summary": "შინაარსი",
        "no_subscriptions": "თქვენ ამ მომენტში არაფერი გაქვთ გამოწერილი. ფიდის გამოსაწერად გამომიგზავნეთ ბმული!",
        "your_subscriptions": "თქვენი გამოწერილები",
        "unsubscribe_prompt": "გაგზავნე ბმული ხელახლა ფიდიდან გამოწერის გასაუქმებლად.",
        "setting_enabled": "ჩართული",
        "setting_disabled": "გამორთული",
    },
}
