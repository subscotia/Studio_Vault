Of course. Here is the first entry for the `VAULT_GUIDE.md`, drafted for clarity and easy reference by any user of the system.

***

## VAULT_GUIDE.md

### **Entry 1: Product vs. Plugin Principle**

**Rule:** The vault operates on a "one plugin, one entry" principle. Each JSON entry must represent a single, individual plugin file (`.vst3`, `.vst2`, etc.), not the entire commercial product package it may have come from.

**Context:** Many software products are sold as bundles or suites. For example, the commercial product "Acustica Crimson" contains multiple individual plugins (a compressor, an EQ, a preamp). A user will always reach for a specific tool (the compressor), not the entire bundle.

**Implementation:**

* **`product` field:** This field should contain the name of the commercial product bundle. For all plugins in the Crimson suite, the value would be `"product": "Acustica Crimson"`.
* **`name` field:** This field must contain the name of the *specific* plugin. For the individual plugins in the Crimson suite, you would have separate entries with `"name": "Crimsoncomp"`, `"name": "Crimsoneq"`, and `"name": "Crimsonpre"`.
* **`id` field:** Each of these individual plugin entries must be assigned its own unique ID. They share a `product` origin, but they are distinct tools in the vault.
* **`families` and `tags`:** These should be assigned based on the specific function of the individual plugin. The `Crimsoncomp` entry would be tagged as a compressor, while the `Crimsoneq` entry would be tagged as an equaliser.


### **Entry 2: Modularity in the `families` Field**

**Rule:** The `families` field must be kept **modular**. Do not create hyper-specific, combined families (e.g., "multiband compressor"). Instead, a plugin's function, technology, and characteristics should be broken down into their individual, reusable components.

**Context:** This approach allows for more powerful and flexible searching of the vault. A user can query for all `"compressors"` or all `"multiband"` tools, rather than needing to know the exact combination for a specific plugin type. A plugin's complete nature is understood by the sum of its family memberships.

**Implementation:**

* A multiband compressor (e.g., FabFilter Pro-MB) should be assigned the families `["compressors", "multiband"]`.
* A multiband limiter should be assigned the families `["limiters", "multiband"]`.
* A hardware emulation of an optical compressor (e.g., an LA-2A model) should be assigned the families `["compressors", "opto", "emulations"]`.

Essentially, if a plugin is a multi-tool, it should be a member of multiple "clubs" or families.



### **Entry 3: Distinction Between "eq" and "equalisers" Families**

**Rule:** A distinction is made between the general `eq` family and the more specific `equalisers` family to allow for more precise tool selection.

**Context:** This system enables a user to perform a broad search for any tool that can shape frequency (`eq`) or a narrow search for a dedicated, full-spectrum tool (`equalisers`).

**Implementation:**

* **`equalisers` Family:** To qualify for this family, a plugin **must** be a dedicated equalization tool that can operate across the full audible frequency spectrum. Its primary purpose is to be an equaliser.
* **`eq` Family:** This is a broader category. A plugin qualifies if it provides any form of frequency-band-specific adjustment, even if it is limited to a narrow part of the spectrum (e.g., a bass enhancement tool with only low-frequency controls).

Crucially, any plugin that qualifies for the **`equalisers`** family **must also** be a member of the **`eq`** family. The reverse is not true.

* *Example:* A full-featured digital EQ would have families including `["equalisers", "eq", "digital"]`.

### **Entry 4: The `type` Field**

**Rule:** The `type` field is a mandatory, single-value field that defines the primary function of a tool. It must be one of the following four values: `"instrument"`, `"container"`, `"fx"`, `"utility"` or '"expansion"'.

**Context:** This classification provides the broadest, most fundamental categorization of a tool in the vault. It is not meant to be as granular as the `families` field. Its purpose is to allow for high-level filtering to quickly isolate a major class of tool.

**Implementation:**

* **`instrument`**: Use for any plugin that generates sound, typically a VSTi. This includes synthesizers, samplers, and romplers.
    * *Example: Spectrasonics Omnisphere*
* **`container`**: Use for any plugin that acts PRIMARILY as a host or shell for other plugins or modules.
    * *Examples: Native Instruments Kontakt, EastWest Opus.*
* **`fx`**: Use for any standard audio effect that processes sound. This is the most common type for non-instrument plugins.
    * *Examples: A reverb, compressor, delay, or equaliser.*
* **`utility`**: Use for any tool whose primary purpose is technical analysis, routing, or workflow assistance, rather than direct sound manipulation.
    * *Examples: A metering plugin, a spectrum analyzer, a gain staging tool, or a connectivity plugin like Blue Cat's Connector.*
**expansion:** This type is for any product that is not a standalone plugin itself, but is a sound library, preset pack, or add-on content designed to be loaded into an existing instrument.

    Entry 5: Clarification on instrument, container, and expansion Types
Rule: A clear distinction must be made between tools that create sound, tools that host other tools, and content that expands existing tools.

Context: Many modern music software products have a modular nature. This guide provides a strict taxonomy to classify these components correctly, ensuring they can be found easily and logically within the vault.

Implementation:

**container:** This type is reserved for a plugin that, on its own, produces no sound and exists only to host other sound-producing libraries or modules.

Primary Example: Native Instruments Kontakt, when loaded without any libraries.

**instrument:** This type is for any plugin that can produce sound "out of the box" with its default installation.

Example: Toontrack's EZDrummer or Superior Drummer, which come with a core sound library.

**expansion:** This type is for any product that is not a standalone plugin itself, but is a sound library, preset pack, or add-on content designed to be loaded into an existing instrument.

Example: An EZX expansion pack for EZDrummer.

The Hierarchy Rule:
The primary function dictates the type.

A tool that can both make sound on its own AND host expansions (like EZDrummer) is classified as an instrument, not a container.

A library that requires a container to function (like a Kontakt library) is classified as an instrument, not an expansion, because the container itself does nothing. The library is the instrument in this context.

Entry 6: ID Naming Convention
Rule: Every object in the master vault must be assigned a unique, permanent ID. This ID is generated programmatically and follows a strict three-part structure to ensure it is both unique and informative.

ID Structure: [Type Code (1)][Developer Code (2)][Sequential Number (5)]

Part 1: Type Code (1 character)
A single uppercase letter representing the object's type key.

I = instrument

X = fx

U = utility

C = container

E = expansion

Part 2: Developer Code (2 characters)
The first two letters of the developer key, converted to uppercase. If the developer name is only a single character, it will be padded with an 'X'.

Part 3: Sequential Number (5 digits)
A globally sequential number that increments for each object in the entire vault, starting from 00001. This number is unique across the whole database and is not reset for different types or developers.

Example:
If the 125th object in the vault is an instrument from "Spitfire Audio", its ID would be:

I (for instrument)

SP (from Spitfire Audio)

00125 (the 125th sequential number)

Final ID: ISP00125