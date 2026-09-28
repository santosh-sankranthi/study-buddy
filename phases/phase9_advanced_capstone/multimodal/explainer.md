# Multimodal Ingestion: Diagrams, Charts, and Vision Models

> **Time:** ~2 min read | **Goal:** Incorporate visual artifacts (diagrams, anatomy charts, mathematical figures) into AI educational pipelines.

---

## 1. Beyond Plain Text

Course notes in STEM subjects are fundamentally visual:
- Biology: Mitosis phases, Krebs cycle flowcharts, cell organelle diagrams.
- Physics: Free-body force vectors, circuit schematics.
- Chemistry: Molecular Lewis structures, reaction pathways.

Standard text extractors extract `[Figure 1]` and throw away the diagram. A student asking *"What is pointing to organelle X in Figure 1?"* gets zero help from plain text.

---

## 2. Ingestion Strategies for Visuals

### Strategy A: Image Captioning & Transcoding (Widely Adopted)
1. At note upload time, extract images and pass them to a vision model (e.g. GPT-4o-mini or Claude 3.5 Sonnet).
2. The vision model outputs a dense technical description:
   *"Diagram showing ATP synthase embedded in the inner mitochondrial membrane, with H+ ions moving from the intermembrane space into the matrix."*
3. This textual caption is chunked and embedded in ChromaDB alongside the main text.

### Strategy B: Multi-Vector / Vision Search (ColPali)
Embeds page screenshots directly into visual-token vector spaces, bypassing OCR entirely.

---

## 3. Formatting Vision Messages

Modern chat completion APIs accept mixed-modality user payloads:
```python
messages = [{
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe this cell diagram for study notes:"},
        {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}
    ]
}]
```
