# Slide Plan Schema

Use this schema for `slide_plan.json`. Keep it simple enough that another
agent can repair it by hand.

## Top Level

```json
{
  "title": "Deck title",
  "mode": "reconstruct_editable",
  "ratio": "16:9",
  "language": "zh-CN",
  "audience": "Prospective buyers",
  "purpose": "Introduce the product",
  "style": {
    "keywords": ["fresh", "minimal", "premium"],
    "palette": {
      "background": "#F7FAF8",
      "primary": "#2FAE91",
      "secondary": "#F2C94C",
      "text": "#16211F",
      "muted": "#6C7A76"
    },
    "font": "Microsoft YaHei"
  },
  "visual_system": {
    "composition": "Large quiet text zone on the left, hero visual on the right",
    "image_style": "Soft daylight, clean product advertising, shallow depth",
    "whitespace": "Reserve at least 40 percent low-detail area for editable text",
    "avoid": ["busy backgrounds", "long embedded text", "fake logos"]
  },
  "visual_prompt_strategy": "visual_prompt_strategy.md",
  "image_prompts": "image_prompts.json",
  "assets": [
    {
      "id": "product_bottle",
      "path": "assets/product_bottle.png",
      "role": "product_cutout"
    }
  ],
  "slides": []
}
```

## Slide Object

```json
{
  "index": 1,
  "type": "cover",
  "title": "Editable title",
  "subtitle": "Editable subtitle",
  "purpose": "What this slide must accomplish",
  "native_shapes": [
    {
      "kind": "oval",
      "box": {"x": 8.2, "y": 0.8, "w": 4.0, "h": 4.0},
      "fill": "#2FAE91",
      "transparency": 72,
      "line": "none"
    },
    {
      "kind": "rounded_rect",
      "box": {"x": 0.55, "y": 0.55, "w": 6.1, "h": 5.8},
      "fill": "#FFFFFF",
      "transparency": 15,
      "line": "#E0ECE8"
    }
  ],
  "image_assets": [
    {
      "asset_id": "product_bottle",
      "box": {"x": 8.8, "y": 1.2, "w": 2.2, "h": 4.8}
    }
  ],
  "text_blocks": [
    {
      "role": "title",
      "text": "Editable title",
      "box": {"x": 0.75, "y": 1.1, "w": 6.2, "h": 0.9},
      "font_size": 38,
      "color": "#16211F"
    },
    {
      "role": "body",
      "text": "Short body copy or bullets",
      "box": {"x": 0.8, "y": 2.4, "w": 5.4, "h": 1.5},
      "font_size": 18,
      "color": "#4E5C58"
    }
  ],
  "visual_notes": "Right-side product hero, soft mint circle, clean blank left area",
  "draft_image": "drafts/slide_01.png",
  "background_image": null,
  "image_prompt": "Prompt used to generate the background visual"
}
```

Coordinates use inches on a 13.333 x 7.5 in 16:9 slide.

## Modes

- `reconstruct_editable`: visual drafts are references; final slides are built
  with native PPT shapes, independent image assets, and editable text.
- `background_plus_text`: final slides may use a full-slide visual background,
  but all readable text remains editable.
- `visual_only`: slides may be flattened images when the user explicitly asks
  for speed or poster-like output.

## Required Fields

- `title`
- `mode`
- `ratio`
- `style.palette`
- `slides[].index`
- `slides[].type`
- `slides[].title`
- `slides[].purpose`
- `slides[].text_blocks`
- `slides[].visual_notes`

In `reconstruct_editable` mode, also include at least one of:

- `slides[].native_shapes`
- `slides[].image_assets`

## Visual Prompt Strategy Links

When image generation is part of the workflow, store the deck-level prompt
strategy and final per-slide prompts beside the slide plan:

- `visual_prompt_strategy`: path to the art-direction and prompt-plan document
- `image_prompts`: path to the exact prompts used for generated draft images

Each slide should also keep its final prompt in `slides[].image_prompt` so a
single slide can be regenerated or repaired without reconstructing the whole
deck context.

## Slide Types

Use these common slide types unless the task calls for something else:

- `cover`
- `section`
- `problem`
- `solution`
- `feature`
- `scenario`
- `process`
- `comparison`
- `specs`
- `summary`
- `closing`

## Native Shape Object

```json
{
  "kind": "rounded_rect",
  "box": {"x": 0.8, "y": 1.4, "w": 4.8, "h": 1.1},
  "fill": "#FFFFFF",
  "transparency": 0,
  "line": "#D9E8E2",
  "line_width": 1
}
```

Supported `kind` values for the helper script:

- `rect`
- `rounded_rect`
- `oval`

Use `line: "none"` for no outline. Transparency is 0-100.

## Image Asset Placement

```json
{
  "asset_id": "leaf_sprig",
  "path": "assets/leaf_sprig.png",
  "box": {"x": 10.8, "y": 5.8, "w": 1.2, "h": 0.8},
  "fit": "contain",
  "rotation": -8
}
```

Use `asset_id` when the asset exists in top-level `assets`; use `path` for
one-off image placements.

Image `fit` values:

- `contain`: preserve aspect ratio and center the image inside the box. This is
  the default and prevents distortion.
- `cover`: preserve aspect ratio, fill the box, and crop evenly from the sides
  or top/bottom. Use for portrait cards or circular avatars.
- `stretch`: force the image to the exact box dimensions. Use only for abstract
  textures or shadows where distortion is intentional.

## Editability Standard

In `reconstruct_editable` mode, `text_blocks` must include every meaningful word
that should appear on the slide, image assets must be movable PPT image objects,
and simple visual structure must be recreated with native shapes. Do not rely
on `draft_image`, `image_prompt`, or `background_image` for readable deck copy.
