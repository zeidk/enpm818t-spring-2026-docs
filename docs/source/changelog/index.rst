====================================================
Changelog
====================================================

All notable changes to the ENPM818T Spring 2026 course documentation are recorded here.



.. dropdown:: v1.0.0 -- Sphinx Build Fixes (2026-02-27)
   :icon: tag
   :class-container: sd-border-success

   Resolved all 197 Sphinx build warnings across lectures 1 through 4.

   .. rubric:: Lecture Files (rubric conversions)

   - **lecture2/lecture.rst**: Converted 43 indented section titles inside ``.. dropdown::`` directives from RST heading syntax to ``.. rubric::`` directives
   - **lecture3/lecture.rst**: Converted 50 indented section titles to ``.. rubric::``; fixed 2 ``:widths:`` mismatches in ``.. list-table::`` directives; extended 6 title underlines to match title length
   - **lecture4/lecture.rst**: Converted 47 indented section titles to ``.. rubric::``

   .. rubric:: Exercise Files (transition removal + icon standardization)

   - **lecture1/exercises.rst**: Removed 6 indented ``----`` transitions; replaced 3 emoji dropdown icons with ``:icon: gear``
   - **lecture2/exercises.rst**: Removed 9 indented ``----`` transitions; replaced 4 emoji dropdown icons with ``:icon: gear``
   - **lecture3/exercises.rst**: Removed 8 indented ``----`` transitions; replaced 4 emoji dropdown icons with ``:icon: gear``
   - **lecture4/exercises.rst**: Removed 12 indented ``----`` transitions; replaced 6 emoji dropdown icons with ``:icon: gear``

   .. rubric:: Quiz Files (transition removal + format restructuring)

   - **lecture1/quiz.rst**: Removed 4 indented ``----`` transitions; restructured from bulk "Answer Key" at bottom to inline ``.. dropdown:: Answer`` after each question (25 questions)
   - **lecture2/quiz.rst**: Removed 2 indented ``----`` transitions; restructured to inline answers (38 questions)

   .. rubric:: Glossary Files (duplicate term removal)

   - **lecture3/glossary.rst**: Removed 6 duplicate term definitions already present in lecture2 glossary (Candidate Key, Composite Key, Crow's Foot Notation, Key Attribute, Logical Data Model, Superkey)
   - **lecture4/glossary.rst**: Removed 2 duplicate term definitions (First Normal Form, Normalization)