# django_news

My first back-end part of this site is made on Python and Django for portfolio.

The front-end code part (HTML, CSS, JS) of the site is taken from [here](https://colorlib.com/wp/template/callie/) for free.

I modified this template:

* Deleted advertisement banners and unused/useless code.
* Created ability to leave comments and answer them.
* Created login form, register form and their sub-forms (forgot password, activation code and etc).

Go to [my site](https://www.fra1t.me/).

## All in one

  1. [Install Docker Compose](https://docs.docker.com/compose/install/).
   2. Clone this repository.
   3. Configure [.env](.env), [config.toml](config.toml) and [uwsgi.ini](uwsgi.ini) files.
   4. Run all containers with `docker-compose up -d`  to launch **django_news**.

## License
[MIT](LICENSE)
