# Paper Structure and Style Guide

## Document Class and Format

- **Document class**: `\documentclass[10pt,twocolumn]{article}`
- **Page margins**: 0.75 inches (professional journal format)
- **Font**: Times (professional serif font)
- **Column separation**: Automatic two-column layout

## Section Structure

### Current Sections (Completed)
1. **Abstract** - Single column, spans both columns
2. **Introduction** - Motivation, contributions, organization
3. **Graph Theory Foundations** - Mathematical definitions
4. **Network Topology Models** - Erdős-Rényi analysis with visualizations

### Planned Sections (Future Work)
5. **Epidemic Simulations** - SIR model implementation
6. **Results and Discussion** - Comparative analysis
7. **Conclusion** - Summary and implications

## Mathematical Notation

### Inline Math
Use `$...$` for inline equations:
- Variables: `$N$`, `$p$`, `$\lambda$`
- Functions: `$P(k)$`, `$\langle d \rangle$`

### Display Math
Use `\begin{equation}...\end{equation}` for numbered equations:
```latex
\begin{equation}
P(k) = \frac{\lambda^k e^{-\lambda}}{k!}
\end{equation}
```

### Common Symbols
- Average/expectation: `$\langle x \rangle$`
- Binomial coefficient: `$\binom{N}{2}$`
- Logarithm: `$\log(N)$`
- Power law: `$k^{-\gamma}$`

## Figure Guidelines

### Single-Column Figures
Use `\begin{figure}[htbp]` for figures within one column.

### Double-Column Figures
Use `\begin{figure*}[t]` for figures spanning both columns (like the phase transition figure).

### Subfigures
```latex
\begin{subfigure}[b]{0.19\textwidth}
    \includegraphics[width=\textwidth]{figures/image.png}
    \caption{Caption text}
    \label{fig:label}
\end{subfigure}
```

### Caption Style
- **Bold title** followed by description
- Reference subfigures as (a), (b), (c)
- Keep captions concise but informative

## References and Citations

### Bibliography Style
Using `\begin{thebibliography}{9}` for simple references.

### Citation Format
```latex
\bibitem{key}
Author(s),
``Title,''
\textit{Journal/Conference}, details, year.
```

### In-text Citations
Use `\cite{key}` to reference: "...as shown in \cite{newman2018networks}"

## Writing Style

### Professional Tone
- Use present tense for general facts
- Use past tense for specific experiments
- Avoid colloquialisms and casual language
- Be precise and concise

### Section Transitions
- Link sections logically
- Reference previous/upcoming sections
- Use forward references: "Section \ref{sec:label}"

### Lists and Enumerations
```latex
\begin{enumerate}[leftmargin=*, itemsep=2pt]
    \item First item
    \item Second item
\end{enumerate}
```

## Compilation Tips

### Multiple Passes
Always compile twice to resolve references:
```bash
pdflatex paper.tex
pdflatex paper.tex
```

### Common Warnings
- Missing references: Run pdflatex twice
- Missing figures: Generate figures first
- Overfull hbox: Adjust wording or hyphenation

### Error Debugging
- Check log file: `paper.log`
- Look for line numbers in error messages
- Ensure all packages are installed

## Best Practices

### Version Control
- Commit after major milestones
- Use meaningful commit messages
- Tag versions before submission

### Collaboration
- Keep figures in separate files
- Use consistent naming conventions
- Document all mathematical notation

### Final Checklist
- [ ] All figures generated and referenced
- [ ] All equations numbered and explained
- [ ] All citations properly formatted
- [ ] Abstract is concise (<250 words)
- [ ] No orphaned headings at page breaks
- [ ] Consistent notation throughout
- [ ] Spell-check completed
- [ ] References complete and accurate
