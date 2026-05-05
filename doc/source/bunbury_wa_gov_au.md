# City of Bunbury

Support for schedules provided by [City of Bunbury](https://www.bunbury.wa.gov.au/live/waste-services/waste-collections).

## Configuration via configuration.yaml

```yaml
waste_collection_schedule:
  sources:
    - name: bunbury_wa_gov_au
      args:
        collection_day: COLLECTION_DAY
        recycling_in_even_week: true
```

### Configuration Variables

**collection_day**
*(string) (required)*

Your bin collection day: `Monday`, `Tuesday`, `Wednesday`, `Thursday`, or `Friday`. Find your day using the Waste Calendar PDF or the City of Bunbury My 3 Bins app, both linked from the [Waste Collections page](https://www.bunbury.wa.gov.au/live/waste-services/waste-collections).

**recycling_in_even_week**
*(boolean) (optional, default: `true`)*

Set to `true` if your recycling bin is collected on even ISO week numbers, `false` if on odd ISO week numbers. Check your last recycling collection date to determine this (use [whatweekisit.org](https://whatweekisit.org/)).

## Example

```yaml
waste_collection_schedule:
  sources:
    - name: bunbury_wa_gov_au
      args:
        collection_day: Wednesday
        recycling_in_even_week: true
```

## How to get the source arguments

1. Visit the [City of Bunbury Waste Collections page](https://www.bunbury.wa.gov.au/live/waste-services/waste-collections) and download the **Waste Calendar PDF**, or download the **City of Bunbury My 3 Bins app**.
2. Locate your address on the collection day map (zones are divided Mon–Fri across the city). Use that day as `collection_day`.
3. To determine `recycling_in_even_week`: note the date of your last recycling collection, look up its ISO week number (e.g. using [whatweekisit.org](https://whatweekisit.org/)), and set `true` if even, `false` if odd.

## Bin types

| Bin | Frequency |
|-----|-----------|
| FOGO (lime green lid) | Weekly |
| Recycling (yellow lid) | Fortnightly |
| Landfill/General waste (red lid) | Fortnightly, alternating with Recycling |
