# CLI 

## Chat 
```bash
litChat chat --data ranavirus_lit.csv 
```

```bash
> Enter you question: how are ranaviruses transmitted? 
[query vector db]
[query gpt]
Ranaviruses are highly infectious and can be transmitted through several routes among amphibians, reptiles, and fish. Here are some common modes of transmission:

Direct Contact: This is the most common method of transmission. The virus can be transmitted directly from one individual to another through contact with skin, mucous membranes, or bodily fluids. [CITE]

Indirect Contact: Ranaviruses can persist in the environment for a certain period of time, especially in water. This allows the virus to be transmitted indirectly when an uninfected individual comes into contact with a contaminated environment or objects. [CITE]

Ingestion: Predators eating infected prey or scavengers eating dead infected animals can contract the virus. [CITE]

Waterborne Transmission: Ranaviruses are often found in aquatic environments, and can be spread through the water, particularly in close, crowded conditions such as those found in aquaculture or in small ponds during breeding aggregations. [CITE]

Vertical Transmission: There's also some evidence that ranaviruses can be transmitted from parent to offspring, although this is less well-studied. [CITE]

It's important to note that the virus can affect a wide range of hosts, and the exact method of transmission can depend on the species involved. Due to their high virulence and the variety of transmission routes, ranaviruses can cause significant disease outbreaks in wildlife populations.
```

## Literature review 

### templates 
Could generate templates from Latex templates.
Database or hub of templates.

```bash
cat review.template 
{TITLE}
{ABSTRACT}
```
The template will be embedded in review writing prompt


### write
```bash
litChat review --data ranavirus_lit.csv --template review.template --title "Ranavirus transmission pathways"
```

## Publish 

Pseudo-journal for LLM generated documents. 

```bash
litChat publish review.md 
[DOI]/URL
```

