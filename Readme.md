# Gist-Wordpress-Sync

A Python application to sync Gists with WordPress.

## Usage

## Notes

### `GistPost()`
The class that hold data collected from gists, to be put into [WordPress post objects](http://python-wordpress-xmlrpc.readthedocs.io/en/latest/ref/wordpress.html#WordPressPost) to be posted.
- `updated_at` is used to check if the latest iteration of the gist has been posted to WordPress.
<br>
The value is stored in the `custom_field` in WordPress.
<br>
[Custom Fields Documentation](http://python-wordpress-xmlrpc.readthedocs.io/en/latest/examples/posts.html?highlight=custom_fields%20)

### `GistBlog()`
- `item` holds the entire gist json payload fetched from api.github.com/gists/
