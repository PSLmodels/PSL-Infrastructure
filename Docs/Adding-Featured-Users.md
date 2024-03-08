# Adding Featured Users

This guide outlines the steps to feature a new user (such as government bodies, academic institutions, or think tanks) on the website. You will need to update the `users.json` file located in the root directory. This file organises featured users into categories and is automatically processed to update the website when changes are committed to the repository.

## File Structure

The `users.json` file is structured into categories like "government", "academic", and "think tanks". Each category contains a list of users with the following properties.

Here is the structure:

```json
{
  "government": [
    {
      "name": "The official name of the user or organisation.",
      "image": "A URL to an image or logo representing the user.",
      "link": "The user's official website or a relevant link."
    }
    // Add more government users here
  ],
  "academic": [
    // Academic users go here
  ],
  "think tanks": [
    // Think tanks users go here
  ]
  // And so on
}
```

## Adding a New User

1. Open the `users.json` file and navigate to the appropriate category. Insert a new object at the end of the list for that category with the user's information.

2. After adding the new user, commit your changes and push them to the repository.

3. The website will automatically update with the new user's information either when the GitHub action is triggered manually or runs on its scheduled daily update.
