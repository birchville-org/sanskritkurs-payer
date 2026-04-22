# Research Summary: Milestone v1.2

## Key Findings

### Search Optimization
We can achieve "Sanskrit-aware" search by customizing the VitePress MiniSearch configuration. By implementing a normalization function (folding diacritics into base ASCII), users can search for Sanskrit terms using standard keyboards without losing the ability to find correctly accented content.

### Automated Indexing
VitePress's `createContentLoader` is the ideal tool for building thematic indexes. We can aggregate tags from frontmatter at build time and render a dynamic "Grammar Navigator" without manual link maintenance.

### i18n Scalability
The project structure is ready for expansion. By modularizing the configuration and extending the existing automated translation pipeline, we can efficiently add Italian and Spanish support.

## Stack Additions
- **VitePress Content Loaders**: For automated metadata aggregation.
- **Custom MiniSearch Tokenizer**: For diacritic folding.
- **Modular Locale Configs**: To manage increasing configuration complexity.

## Watch Out For
- **Translation Drift**: Ensuring all 4 languages stay in sync.
- **Search Over-folding**: Balancing search ease-of-use with phoneme precision.
- **Sidebar Bloat**: Keeping navigation manageable as the site grows.
