{% extends "mail_templated/base.tpl" %}

{% block subject %}
Email Verification
{% endblock %}

{% block html %}
<h3>Hello dear {{user}}</h3>
<!-- <img src="https://static.vecteezy.com/packs/media/components/global/search-explore-nav/img/vectors/term-bg-1-666de2d941529c25aa511dc18d727160.jpg"> -->
<h4>click below to verify your email and active your account:</h4>
http://127.0.0.1:8000/accounts/api-v1/confirm-verification/{{token}}/
{% endblock %}