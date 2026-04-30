# Post Library

Every piece of social content generated through the magnitude-social-content (or dsg-social-content) skill is saved here. This is the active asset bank — find finished posts and reuse them.

## Structure

```
library/posts/
  magnitude/    Magnitude Finance branded posts
    YYYY-MM-DD-[slug]/
      post.md   FCA compliance record (copy, vars, platform, date)
      card.png  Rendered PNG — the image you actually post
  dsg/          DSG Financial Services branded posts (future)
```

## FCA compliance

As a regulated firm (FRN: 649675), DSG Financial Services Ltd needs to be able to evidence its marketing communications. The `post.md` in each folder is that evidence — it records the date, pillar, platform, full copy as posted, and the variables passed to hcti.io.

## Do not delete folders from this library

These are compliance records. If a post is superseded, add a note in its `post.md` — don't delete the folder.
