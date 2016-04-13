---
layout: default
title: "Home"
teaser: ""
breadcrumb: true
header: false
permalink: "/"
---
<div id="blog-index" class="row">
	<div class="small-12 columns t30">
		
		<dl class="accordion" data-accordion>
			{% assign counter = 1 %}
			{% for post in site.posts reversed limit:1000 %}
			<dd class="accordion-navigation">
            <a href="{{ site.url }}{{ post.url }}"><span class="iconfont"></span> <strong>{{ post.title }}</strong>{% if post.subheadline %} </br>{{ post.subheadline }}{% endif %}</a>
              
            </dd>
			{% assign counter=counter | plus:1 %}
			{% endfor %}
		</dl>
	</div><!-- /.small-12.columns -->
</div><!-- /.row -->
