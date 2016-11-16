# Gist-Wordpress-Sync

A Python application to sync Gists with WordPress.

Example : http://hacks.ash.wine

## Requirements

- Python 2.7+
- [Python-Wordpress-xmlrpc](http://python-wordpress-xmlrpc.readthedocs.io/en/latest/index.html) library.

    `pip install python-wordpress-xmlrpc`

## Usage
1. Clone or download this repository.
2. Rename the `.setting.example` file to `.setting` and configure the variables.<br>Example:
```
WORDPRESS_URL=http://my-wordpress-blog.com
WORDPRESS_USERNAME=wordpress_username
WORDPRESS_PASSWORD=wordpress_pasword
GITHUB_USERNAME=github_username
```
3. Optionally you can add a `GITHUB_ACCESS_TOKEN` (for higher rate limits etc.) and a `WORDPRESS_CATEGORY` if you want to sync content with a particular category in your blog.
4. In the description of the gists you want to sync, add `#gistblog`.
5. You can additionally add other hashtags to your description, those will be parsed over to Wordpress as tags for the post.
6. In your wordpress header, link the CSS required to correctly highlight/display code snippets and content.
```CSS
<link crossorigin="anonymous" href="https://assets-cdn.github.com/assets/frameworks-31e369ccd2b23a1eccde83f03ef36eafff1f7b9025f6042ccac33a7915753de2.css" integrity="sha256-MeNpzNKyOh7M3oPwPvNur/8fe5Al9gQsysM6eRV1PeI=" media="all" rel="stylesheet" />
<link crossorigin="anonymous" href="https://assets-cdn.github.com/assets/github-f52c8c687f8b759e77e94e3641edb1c5f49d6e8e0738ef162a66361316566cff.css" integrity="sha256-9SyMaH+LdZ536U42Qe2xxfSdbo4HOO8WKmY2ExZWbP8=" media="all" rel="stylesheet" />
```
7. Run `python Gist-Wordpress-Sync-2.py`

## Notes

The biggest downside currently is that the application needs to be manually invoked everytime changes need to be synced. (This is because webhooks/events are not available on gists.)

In the future, this app could potentially be compiled and bundled as a wordpress plugin, which can then be run as cron job to sync posts and gists.

## Function Reference

### `GistPost()`
The class that hold data collected from gists, to be put into [WordPress post objects](http://python-wordpress-xmlrpc.readthedocs.io/en/latest/ref/wordpress.html#WordPressPost) to be posted.
- `updated_at` is used to check if the latest iteration of the gist has been posted to WordPress.
<br>
The value is stored in the `custom_field` in WordPress.
<br>
[Custom Fields Documentation](http://python-wordpress-xmlrpc.readthedocs.io/en/latest/examples/posts.html?highlight=custom_fields%20)

### `GistBlog()`
- `item` holds the entire gist json payload fetched from api.github.com/gists/
