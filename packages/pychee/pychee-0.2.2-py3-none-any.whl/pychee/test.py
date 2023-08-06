import pychee
client = pychee.LycheeClient('https://pic.chosto.me')
client.login('Chosto', 'TWM4W3APC9J2Oczn2RSeb6tmoPJYyUMQVNAtqDvh')

# Create a new album
album_name = 'test_name'
album_id = client.add_album(album_name)['id']

# Add a photo in the created album
path_to_your_photo = '/home/images/screenshots/2023-02-19_19-48.png'
with open(path_to_your_photo, 'rb') as f:
    photo_id = client.add_photo(f, 'photo.jpg', album_id)['id']

# Set uploaded photo public
client.set_photo_public(photo_id)

# Set licence of uploaded photo
client.set_photo_license(photo_id, 'CC0')

# Download an archive of the created album
output_path = '/tmp/photos.zip'
with(open(output_path, 'wb')) as f:
     f.write(client.get_albums_archive([album_id]))

# Logout
client.logout()