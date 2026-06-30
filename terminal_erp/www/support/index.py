import terminal_framework
from terminal_framework.query_builder.functions import Count, Max


def get_context(context):
	context.no_cache = 1
	context.align_greeting = ""
	setting = terminal_framework.get_doc("Support Settings")

	context.greeting_title = setting.greeting_title
	context.greeting_subtitle = setting.greeting_subtitle

	# Support content
	favorite_articles = get_favorite_articles_by_page_view()
	if len(favorite_articles) < 6:
		name_list = []
		if favorite_articles:
			for article in favorite_articles:
				name_list.append(article.name)
		for record in terminal_framework.get_all(
			"Help Article",
			fields=["title", "content", "route", "category"],
			filters={"name": ["not in", tuple(name_list)], "published": 1},
			order_by="creation desc",
			limit=(6 - len(favorite_articles)),
		):
			favorite_articles.append(record)

	context.favorite_article_list = get_favorite_articles(favorite_articles)
	context.help_article_list = get_help_article_list()


def get_favorite_articles_by_page_view():
	ha = terminal_framework.qb.DocType("Help Article")
	wpv = terminal_framework.qb.DocType("Web Page View")
	return (
		terminal_framework.qb.from_(ha)
		.inner_join(wpv)
		.on(ha.route == wpv.path)
		.select(
			# route is the unique page URL, so there is one published article per route: Max() just
			# returns that row's columns while keeping the GROUP BY route valid on postgres
			Max(ha.name).as_("name"),
			Max(ha.title).as_("title"),
			Max(ha.content).as_("content"),
			ha.route,
			Max(ha.category).as_("category"),
			Count(ha.route).as_("count"),
		)
		.where(ha.published == 1)
		.groupby(ha.route)
		.orderby(Count(ha.route), order=terminal_framework.qb.desc)
		.limit(6)
		.run(as_dict=True)
	)


def get_favorite_articles(favorite_articles):
	favorite_article_list = []
	for article in favorite_articles:
		description = terminal_framework.utils.strip_html(article.content)
		if len(description) > 120:
			description = description[:120] + "..."
		favorite_article_dict = {
			"title": article.title,
			"description": description,
			"route": article.route,
			"category": article.category,
		}
		favorite_article_list.append(favorite_article_dict)
	return favorite_article_list


def get_help_article_list():
	help_article_list = []
	category_list = terminal_framework.get_all("Help Category", fields="name")
	for category in category_list:
		help_articles = terminal_framework.get_all(
			"Help Article",
			fields="*",
			filters={"category": category.name, "published": 1},
			order_by="creation desc",
			limit=5,
		)
		if help_articles:
			help_aricles_per_caetgory = {
				"category": category,
				"articles": help_articles,
			}
			help_article_list.append(help_aricles_per_caetgory)
	return help_article_list
