# Design

Previews and demos are rendered from `tools/worlds/<world>.html.j2`, picked by the spec's `world` field (`tools/lead_preview.py` maps each trade). Each world is its own visual system, not a recolour.

| World | Trades | Material | Type | One moment |
|---|---|---|---|---|
| `docket` | cafés, restaurants, bakeries, bars, takeaway | Kitchen order dockets clipped to a steel rail; carbon-book yellow and pink; blue biro notes; menu as a long receipt | Big Shoulders Display, Courier Prime, Reenie Beanie | Hero dockets swing to rest on the rail |
| `formula` | hair, beauty, tattoo, massage | Ruled index card on a plum colour-bar ground; hair-swatch tufts; services as typed formulas with tube chips | Gloock, Hanken Grotesk, Martian Mono | Swatch tufts fan out |
| `tape` | trades, auto, hire, bikes | Yellow tape blade with graduations; sections sit at red marks on a vertical rule; phone number big in black | Barlow Condensed, Barlow | Graduations pull out across the hero |
| `poster` | shops, clinics, offices (`tone: calm` for clinics and professional services) | Wire-framed newsagent bill posters with a masthead strip and one huge factual headline | League Gothic, Libre Franklin | Headline tracking settles |

Rules for every world: only facts from the listing (name, address, phone, hours, trade); the call action sits in the hero and the fixed phone bar; licensed photos keep their credits; previews stay noindex and labelled; motion switches off under reduced motion.
