Structure of a Seed Nugget

Every seed nugget has the same five layers. This consistency makes the archive navigable and the template maintainable. A reader who knows the structure can find what they need at whatever depth they want.

### Layer 1: Surface

The accessible version. Written for a curious high schooler or a first-time encounter with the idea. Concrete language, relatable examples, no jargon. Goal: recognition — oh, I've felt that, I just didn't have words for it. Ends with a call to action: "try this" or "look for this." Length: 400–700 words. Test with real young readers.

### Layer 2: Depth

The intellectual version. Connects to philosophy, science, history of ideas. Where Whitehead, Gödel, autopoiesis, and the rest live. Does not dumb down — assumes a reader who wants to go further. Can include technical detail. References other seeds by number. Length: 300–600 words.

### Layer 3: Provenance

The roots. Glossary of key terms with definitions. Bibliography with full citations. Intellectual lineage — whose ideas these are, where they came from, what to read next. Intellectual honesty baked into the structure. Not a footnote — a genuine resource for the curious reader.

### Layer 4: Script

The three-minute video version. Written as a shooting script with direction lines (in caps or italic) and spoken text. Designed for compression and emotional landing — the seed as a short piece of entertainment that arrives before it explains. Inspired by Jason Silva's style: rapid, evocative, philosophically serious. Ends with a single sharp question or image.

### Layer 5: Images

The visual language. Describes (and eventually will contain) illustrations, animation concepts, shareable graphics. Each seed should have: a primary illustration, a shareable one-line graphic for social media, and a video thumbnail concept. The images should be able to stand alone and still transmit something of the seed's essence.

### Additional fields

Each seed also carries: number (permanent identifier), short name (used in filename and URL), title, subtitle (one sentence), status (empty / partial / draft1 / final), date added, tags, and related seeds (up to five, by number). These are stored in the source .txt file and used to build the repository and navigation automatically.

---


## Nugget file grammar 
(for drop-in compatibility)

The build script parses nugget files strictly. Follow this grammar so new or revised nuggets work without manual processing.

**File**

- Location: `nuggets/` directory.
- Name: `NNN-shortname.txt` where NNN is the 3-digit zero-padded number (e.g. 001, 020) and shortname matches the `#shortname` value. Lowercase, no spaces.
- Encoding: UTF-8.

**Structure (order is fixed)**

1. Metadata block: single-line fields, one per line.
2. Layer block: exactly five sections, in this order — surface, depth, provenance, script, images. Each section is a line `#layername` (no value) followed by the section body until the next line that starts with `#`.

**Metadata (single-line fields)**

- Each line: `#fieldname value` (one space after the hash, field name, space, rest of line is value).
- Field names are case-insensitive; the parser lowercases them.
- Required fields and format:
  - `#number` — exactly the nugget id. Use 3-digit zero-padding (001, 002, … 020, 021). Must match the NNN in the filename.
  - `#shortname` — one word or hyphenated phrase, lowercase, no spaces (e.g. caloric, inside, past-present). Must match the shortname in the filename.
  - `#title` — full title; may contain spaces and punctuation.
  - `#subtitle` — one sentence; may contain spaces and punctuation.
  - `#status` — exactly one of: empty | partial | draft1 | final
  - `#date` — date string (e.g. 2026-03-11).
  - `#tags` — comma-separated list. Each tag: lowercase, multi-word tags hyphenated (e.g. history-of-science, AI). No spaces after commas required but allowed.
  - `#related` — comma-separated list of other nugget numbers. Use the same string as each target nugget’s `#number` (e.g. 002, 011, 018). Max 5. Links resolve by string equality, so "1" will not match a nugget whose `#number` is "001".

**Layers (multi-line sections)**

- Section start: a line that is exactly `#surface`, `#depth`, `#provenance`, `#script`, or `#images` (no text after the name). Parser treats these as layer names, not metadata.
- Section body: all following lines that do not start with `#`. Blank lines are kept. Body ends at the next line starting with `#` or end of file.
- All five layer headers must appear in this order: `#surface`, `#depth`, `#provenance`, `#script`, `#images`. If a layer has no content yet, write the header and put `TBD` (or a single line of placeholder text) as the body so the section exists.
- Layer content is free-form text. No special syntax required. Use `TBD` for placeholder sections.

**Parsing rules (what the build does)**

- Lines starting with `#`: after the `#`, the first token is the key; the rest of the line (after the first run of whitespace) is the value. Keys in the metadata set (number, shortname, title, subtitle, status, date, tags, related) are stored as meta; value is trimmed. Any other key starts a layer and subsequent non-`#` lines are appended to that layer’s body.
- Tags: meta["tags"] is split on commas, each item stripped.
- Related: meta["related"] is split on commas, each item stripped. Matching to other nuggets is by exact string equality of `#number`.

**Minimal valid nugget (template)**
```
#number 999
#shortname example
#title Example Title
#subtitle One sentence subtitle.
#status empty
#date 2026-03-11
#tags tag-one, tag-two
#related 001, 002

#surface
TBD

#depth
TBD

#provenance
TBD

#script
TBD

#images
TBD
```
Save as `nuggets/999-example.txt` (number and shortname must match filename).
