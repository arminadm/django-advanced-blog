{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{ user.name }}
{% endblock %}

{% block html %}
<h3>Hello dear {{user}}</h3>
<!-- <img src="https://static.vecteezy.com/packs/media/components/global/search-explore-nav/img/vectors/term-bg-1-666de2d941529c25aa511dc18d727160.jpg"> -->
<h4>here is your token:</h4>
{{token}}
{% endblock %}