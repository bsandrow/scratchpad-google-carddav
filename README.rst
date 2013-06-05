===============
google-contacts
===============

My scratchpad for messing with Google Contacts.

Notes:
------
 - URL => "https://google.com/m8/carddav/principals/__uids__/{user}/lists/default/"
 - {user} => E.g. 'user@gmail.com'
 - {user} can be 'default' to refer to the currently authenticated user
 - "PROPFIND https://google.com/m8/carddav/principals/__uids__/{user}/lists/"
   seems to return the same info as if the 'default/' was at the end.
 - Technically you can use "PROPFIND https://google.com/m8/carddav", which will
   list the url paths under it.
 - If you know the UID of the contact, you can fetch that contact via
   "BASE_URL/{user}/lists/default/{UID}" even if it's not in "My Contacts"
 - Looks like only contacts in "My Contacts" will be listed via CardDAV
 - Looks like using REPORT and an address book query returns 404
