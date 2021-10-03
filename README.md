# Leanpub multi-action

Interact with Leanpub via GitHub Actions

## Inputs

### `leanpub-api-key`

**Required** The Leanpub API key for your account, which requires a "Pro" plan on Leanpub.com.
Recommended to place this in a GitHub Secret named `LEANPUB_API_KEY`.

### `leanpub-book-slug`

**Required** The "slugified" name of your book, i.e. "mygreatbook" for "My Great Book".
Per Leanpub's [API documentation](https://leanpub.com/help/api), it is "the part of the URL for your book after `https://leanpub.com/"`.

### `preview`

Boolean, set to "true" to trigger a Leanpub Preview generation for your book.

## Example Usage

Below is an example workflow file:

```YAML
# This is the GH Action file to trigger a preview on push event to a branch named "Preview"
---
name: "Push to Preview"

"on":
  push:
    branches: ["preview"]
  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch: null

jobs:
  preview_build:
    runs-on: "ubuntu-latest"
    steps:
      # Kick off a preview
      - name: "Preview Build"
        uses: "lykinsbd/leanpub-multi-action@v1.0.2
"
        with:
          leanpub-api-key: "${{secrets.LEANPUB_API_KEY}}"
          leanpub-book-slug: "mygreatbook"
          preview: true

```
