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
            <a href="#panel{{ counter }}"><span class="iconfont"></span> <strong>{{ post.title }}</strong>{% if post.subheadline %} </br>{{ post.subheadline }}{% endif %}</a>
            {{ site.url }}{{ post.url }}
              <div id="panel{{ counter }}" class="content">
                {% if post.meta_description %}{{ post.meta_description | strip_html | escape }}{% elsif post.teaser %}{{ post.teaser | strip_html | escape }}{% elsif post.excerpt %}{{ post.excerpt }}{% endif %}
                <a href="{{ site.url }}{{ post.url }}" title="Read {{ post.title escape_once }}"><strong>{{ site.data.language.read_more }}</strong></a><br><br>
              </div>
            </dd>
			{% assign counter=counter | plus:1 %}
			{% endfor %}
		</dl>
	</div><!-- /.small-12.columns -->
</div><!-- /.row -->
