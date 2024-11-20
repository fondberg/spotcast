# Obtaining `sp_dc` and `sp_key` cookies

Spotcast uses two cookies to authenticate against Spotify in order to have access to register devices on an account.

To obtain the cookies, these different methods can be used:

## Chrome based browser

### Chrome web console

1. Open a new __Incognito window__ at [`https://open.spotify.com`](https://open.spotify.com) and login to Spotify.
2. Press `Command+Option+I` (Mac) or `Control+Shift+I` or `F12`. This should open the developer tools menu of your browser.
3. Go into the `application` section.
4. In the menu on the left go int `Storage/Cookies/open.spotify.com`.
5. Find the `sp_dc` and `sp_key` and copy the values.
6. Close the window without logging out (Otherwise the cookies are made invalid).

![cookie in chrome developer tools](images/cookies_chrome_2.png)

## Firefox based browser

### Firefox web console

1. Open a new __Incognito window__ at [`https://open.spotify.com`](https://open.spotify.com) and login to Spotify.
2. Press `Command+Option+I` (Mac) or `Control+Shift+I` or `F12`. This should open the developer tools menu of your browser.
3. Go into the `Storage` section. (You might have to click on the right arrows to reveal the section).
4. Select the `Cookies` sub-menu and then `https://open.spotify.com`.
5. Find the `sp_dc` and `sp_key` and copy the values.
6. Close the window without logging out (Otherwise the cookies are made invalid).

![Firefox developer tool](images/cookies_firefox_1.png)
