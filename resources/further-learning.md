# Further Learning Resources for Workflow Tools

This document provides curated links to official documentation, tutorials, community forums, example repositories, and academic papers for all five workflow management tools covered in this seminar.

## GNU Parallel

### Official Documentation
- [GNU Parallel Official Manual](https://www.gnu.org/software/parallel/) - Comprehensive reference guide
- [GNU Parallel Tutorial](https://www.gnu.org/software/parallel/parallel_tutorial.html) - Getting started with basic concepts
- [GNU Parallel Examples](https://www.gnu.org/software/parallel/man.html) - Detailed examples and common patterns
- [GNU Parallel Bash Integration](https://www.gnu.org/software/parallel/sql.html) - Integration with shell scripting

### Tutorials and Guides
- [GNU Parallel Quick Reference](https://www.gnu.org/software/parallel/env_parallel.html) - Common use cases and quick examples
- [Parallel Processing with GNU Parallel](https://xed.ch/help/parallel) - Third-party tutorial with practical examples
- [O'Reilly Guide to GNU Parallel](https://www.oreilly.com/library/view/parallel-command-line-tools/9781491989449/) - Comprehensive book reference

### Community and Support
- [GNU Parallel Mailing List](https://lists.gnu.org/mailman/listinfo/parallel) - Official discussion forum
- [Stack Overflow: gnu-parallel tag](https://stackoverflow.com/questions/tagged/gnu-parallel) - Community Q&A
- [GitHub: GNU Parallel Issues](https://git.savannah.gnu.org/git/parallel.git/) - Official source repository

### Example Repositories
- [GNU Parallel Examples Repository](https://git.savannah.gnu.org/git/parallel.git/tree/examples) - Official examples
- [NERSC Parallel Processing Guide](https://docs.nersc.gov/jobs/workflow/) - HPC-specific guidance

---

## signac

### Official Documentation
- [signac Official Documentation](https://docs.signac.io/) - Complete user guide and API reference
- [signac Project Configuration](https://docs.signac.io/en/latest/configuration.html) - Setting up projects
- [signac-flow Workflow Guide](https://docs.signac.io/projects/flow/en/latest/) - Defining and executing workflows
- [signac API Reference](https://docs.signac.io/en/latest/module.html) - Detailed API documentation

### Tutorials and Getting Started
- [signac Quick Start](https://docs.signac.io/en/latest/quickstart.html) - Five-minute introduction
- [signac Data Model Tutorial](https://docs.signac.io/en/latest/tutorial.html) - Understanding the data model
- [signac-flow Job Submission](https://docs.signac.io/projects/flow/en/latest/submission.html) - HPC job submission
- [Parameter Space Design](https://docs.signac.io/en/latest/signac-identify.html) - Organizing complex parameter studies

### Community and Support
- [signac Discourse Community](https://discourse.signac.io/) - Main community forum
- [signac GitHub Discussions](https://github.com/glotzerlab/signac/discussions) - GitHub community space
- [signac Issues and Bug Reports](https://github.com/glotzerlab/signac/issues) - Project issue tracker
- [signac Slack Community](https://signac-project.slack.com/) - Real-time chat (join via website)

### Example Repositories
- [signac Examples Repository](https://github.com/glotzerlab/signac-examples) - Official example workflows
- [signac Tutorials Repository](https://github.com/glotzerlab/signac-tutorials) - Step-by-step learning projects
- [NERSC signac Integration](https://docs.nersc.gov/programming/high-level-languages/python/#signac) - HPC-specific guidance

### Academic and Research
- [signac Paper: Toward Reproducible Workflows](https://doi.org/10.1016/j.cpc.2021.107901) - Published research on reproducibility
- [Parameter Study Management with signac](https://arxiv.org/abs/1907.10905) - Research paper on design patterns

---

## Maestro

### Official Documentation
- [Maestro Official Documentation](https://maestrowf.readthedocs.io/) - Complete user guide
- [Maestro Specification Reference](https://maestrowf.readthedocs.io/en/latest/spec_reference.html) - YAML specification details
- [Maestro Workflow Definition](https://maestrowf.readthedocs.io/en/latest/maestro_spec.html) - How to define workflows
- [Maestro Study Management](https://maestrowf.readthedocs.io/en/latest/study_management.html) - Managing study execution

### Tutorials and Getting Started
- [Maestro Quick Start Guide](https://maestrowf.readthedocs.io/en/latest/getting_started.html) - Five-minute introduction
- [Maestro Basic Examples](https://maestrowf.readthedocs.io/en/latest/examples.html) - Simple to complex examples
- [Maestro Environment Configuration](https://maestrowf.readthedocs.io/en/latest/environments.html) - Setting up HPC environments
- [Batch Block Configuration](https://maestrowf.readthedocs.io/en/latest/batch_scheduling.html) - Job submission patterns

### Community and Support
- [Maestro GitHub Repository](https://github.com/LLNL/maestrowf) - Main project repository
- [Maestro GitHub Issues](https://github.com/LLNL/maestrowf/issues) - Bug reports and feature requests
- [Maestro GitHub Discussions](https://github.com/LLNL/maestrowf/discussions) - Community discussions
- [LLNL Software Community](https://computing.llnl.gov/projects/maestro) - LLNL project information

### Example Repositories
- [Maestro Examples Directory](https://github.com/LLNL/maestrowf/tree/develop/examples) - Official examples
- [Maestro Study Templates](https://github.com/LLNL/maestrowf/tree/develop/maestrowf/samples) - Pre-built templates
- [NERSC Maestro Integration](https://docs.nersc.gov/jobs/workflow/) - NERSC-specific guidance

### Academic and Research
- [Maestro: Workflow Orchestration](https://computing.llnl.gov/projects/maestro/overview) - Project overview and citations
- [Workflow Management for Parameter Studies](https://arxiv.org/abs/1702.00060) - Related research on study management

---

## Merlin

### Official Documentation
- [Merlin Official Documentation](https://merlin.readthedocs.io/) - Complete user guide and API reference
- [Merlin Specification Guide](https://merlin.readthedocs.io/en/latest/user_guide/specification.html) - YAML specification
- [Merlin Workflow Execution](https://merlin.readthedocs.io/en/latest/user_guide/running_workflows.html) - Running and monitoring workflows
- [Merlin CLI Reference](https://merlin.readthedocs.io/en/latest/user_guide/command_line.html) - Command-line interface

### Tutorials and Getting Started
- [Merlin Quick Start](https://merlin.readthedocs.io/en/latest/getting_started.html) - Getting started in minutes
- [Merlin Basic Tutorial](https://merlin.readthedocs.io/en/latest/tutorials.html) - Step-by-step tutorials
- [Merlin Parameter Study Design](https://merlin.readthedocs.io/en/latest/user_guide/parameters.html) - Defining parameter spaces
- [Merlin Results Processing](https://merlin.readthedocs.io/en/latest/user_guide/post_processing.html) - Analyzing workflow results

### Infrastructure and Advanced Topics
- [Merlin Parallel Execution](https://merlin.readthedocs.io/en/latest/user_guide/celery.html) - Celery worker configuration
- [Merlin Database Setup](https://merlin.readthedocs.io/en/latest/user_guide/database.html) - Database configuration (Redis/PostgreSQL)
- [Merlin Server Monitoring](https://merlin.readthedocs.io/en/latest/user_guide/monitoring.html) - Workflow monitoring tools
- [Merlin on HPC Systems](https://merlin.readthedocs.io/en/latest/user_guide/systems.html) - HPC-specific configuration

### Community and Support
- [Merlin GitHub Repository](https://github.com/LLNL/merlin) - Main project repository
- [Merlin GitHub Issues](https://github.com/LLNL/merlin/issues) - Bug reports and feature tracking
- [Merlin GitHub Discussions](https://github.com/LLNL/merlin/discussions) - Community support
- [LLNL Computing Center](https://computing.llnl.gov/) - LLNL project information

### Example Repositories
- [Merlin Examples Directory](https://github.com/LLNL/merlin/tree/develop/examples) - Official workflow examples
- [Merlin Demo Workflows](https://github.com/LLNL/merlin/tree/develop/demos) - Demonstration projects
- [Merlin Integration Examples](https://github.com/LLNL/merlin/tree/develop/tests) - Integration and testing examples

### Academic and Research
- [Merlin Paper: Large-Scale Workflow Management](https://computing.llnl.gov/projects/merlin/overview) - Project overview
- [Distributed Workflow Management](https://arxiv.org/abs/1810.01851) - Research on distributed workflows

---

## AiiDA

### Official Documentation
- [AiiDA Official Documentation](https://aiida.readthedocs.io/) - Comprehensive user guide
- [AiiDA Installation Guide](https://aiida.readthedocs.io/en/latest/install/index.html) - Installation and setup
- [AiiDA Workflows](https://aiida.readthedocs.io/en/latest/topics/workflows/index.html) - Workflow definition and execution
- [AiiDA Database](https://aiida.readthedocs.io/en/latest/topics/database/index.html) - Database architecture and usage

### Tutorials and Getting Started
- [AiiDA Quick Start](https://aiida.readthedocs.io/en/latest/intro/get_started.html) - Getting started guide
- [AiiDA Workflow Tutorial](https://aiida.readthedocs.io/en/latest/tutorials/index.html) - Comprehensive tutorials
- [AiiDA Provenance and Lineage](https://aiida.readthedocs.io/en/latest/topics/provenance/index.html) - Understanding provenance tracking
- [AiiDA Data Model](https://aiida.readthedocs.io/en/latest/topics/data_types/index.html) - Data model and structures

### Infrastructure and Advanced Topics
- [AiiDA Computer Configuration](https://aiida.readthedocs.io/en/latest/topics/computers/index.html) - Setting up remote computers
- [AiiDA Code Management](https://aiida.readthedocs.io/en/latest/topics/codes/index.html) - Registering and managing codes
- [AiiDA Job Submission](https://aiida.readthedocs.io/en/latest/topics/scheduler/index.html) - Job scheduler integration
- [AiiDA SSH/SFTP Transport](https://aiida.readthedocs.io/en/latest/topics/transport/index.html) - Remote execution

### Community and Support
- [AiiDA Community Forum](https://discourse.aiida.net/) - Official community forum
- [AiiDA GitHub Repository](https://github.com/aiidateam/aiida-core) - Main project repository
- [AiiDA GitHub Discussions](https://github.com/aiidateam/aiida-core/discussions) - Community discussions
- [AiiDA Slack Community](https://aiida.slack.com/) - Real-time chat (register on website)

### Example Repositories
- [AiiDA Examples Repository](https://github.com/aiidateam/aiida-examples) - Official examples
- [AiiDA Plugins Registry](https://aiida.readthedocs.io/en/latest/plugins/index.html) - Available plugins and extensions
- [AiiDA Quantum ESPRESSO Plugin](https://github.com/aiidateam/aiida-quantumespresso) - Popular example plugin
- [AiiDA SIESTA Plugin](https://github.com/aiidateam/aiida-siesta) - Another example plugin

### Academic and Research
- [AiiDA Paper: Automated Interactive Infrastructure](https://doi.org/10.1038/s41524-020-00472-7) - Main AiiDA paper
- [Provenance in Computational Science](https://doi.org/10.1038/ncomms14357) - Research on provenance tracking
- [Reproducible Science Workflows](https://arxiv.org/abs/2010.11953) - Workflow management research
- [Materials Science Workflows](https://www.nature.com/articles/s41467-019-14030-3) - Domain-specific applications

---

## Cross-Tool Resources

### Workflow Management Concepts
- [Workflow Management Systems Survey](https://arxiv.org/abs/2210.02840) - Comprehensive survey of workflow systems
- [Parallel Computing Patterns](https://www.apress.com/us/book/9781430243664) - Common patterns in parallel workflows
- [Reproducible Research in Computational Science](https://science.sciencemag.org/content/334/6060/1226) - Best practices for reproducibility

### HPC and NERSC-Specific Resources
- [NERSC User Portal](https://www.nersc.gov/) - Main NERSC information
- [NERSC Perlmutter Documentation](https://docs.nersc.gov/systems/perlmutter/) - Perlmutter-specific guidance
- [NERSC Job Scheduling Guide](https://docs.nersc.gov/jobs/) - Slurm and job submission
- [NERSC Workflow Tools](https://docs.nersc.gov/jobs/workflow/) - NERSC's workflow documentation
- [NERSC Profiling and Performance](https://docs.nersc.gov/tools/performance/) - Performance optimization

### Git and Version Control
- [Git Basics for Workflows](https://git-scm.com/book/en/v2) - Understanding version control
- [GitHub Workflow Best Practices](https://docs.github.com/en/get-started/quickstart) - Collaborative development
- [Reproducible Science with Git](https://swcarpentry.github.io/git-novice/) - Software Carpentry curriculum

### Containers and Reproducibility
- [Docker for Workflow Reproducibility](https://docs.docker.com/get-started/) - Container basics
- [Singularity HPC Containers](https://sylabs.io/docs/) - Container guide for HPC
- [Reproducible Environments](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html) - Creating reproducible computing environments

---

## Books and Reference Materials

### Workflow Management
- "Parallel Command-Line Tools" (O'Reilly, 2018) - Comprehensive guide to command-line parallelization
- "High Performance Computing" (Pacheco, 2011) - Foundational HPC concepts
- "Designing HPC Applications" (Lucas, 2015) - Design patterns for HPC workflows

### Scientific Computing
- "Computational Science and Engineering" (Strang, 2007) - Computational methods
- "Understanding Scientific Software" (Rouson, 2011) - Software engineering for science
- "The Art of HPC" (Eijkhout, ongoing) - Free HPC reference manual

---

## Staying Current

### Conference Proceedings
- [ECP Annual Meetings](https://www.exascaleproject.org/) - Exascale Computing Project
- [SC Conference Series](https://sc23.supercomputing.org/) - International HPC conference
- [PEARC Conference](https://www.pearc21.pearc.acm.org/) - Practice & Experience in Advanced Research Computing

### Journals and Publications
- [ACM Transactions on Mathematical Software](https://toms.acm.org/) - HPC software papers
- [The International Journal of High Performance Computing Applications](https://journals.sagepub.com/home/hpc) - HPC research
- [Nature Computational Science](https://www.nature.com/natcomputsci/) - Computational science research

### Newsletters and Blogs
- [NERSC News](https://www.nersc.gov/news-and-publications/newsletters/) - NERSC updates
- [Lawrence Livermore Lab Computing](https://computing.llnl.gov/) - LLNL research and tools
- [HPC User Forum](https://www.hpcuserforum.com/) - Community updates

---

## Getting Help

### Debugging and Troubleshooting
- See `resources/troubleshooting.md` for common issues and solutions for each tool
- See `resources/comparison-matrix.md` for tool differences that may explain unexpected behavior
- Review example code in each tool's examples directory

### Choosing the Right Tool
- See `resources/decision-tree.md` for guidance on selecting appropriate tools
- See `resources/comparison-matrix.md` for detailed feature and capability comparison
- Consult the "sweet spot" section for each tool's optimal use cases

### Running on Perlmutter
- See `resources/nersc-best-practices.md` for NERSC-specific configuration and anti-patterns
- Check `resources/installation-guides/` for per-tool setup instructions
- Review example sections in main documentation (00-gnu-parallel through 03-merlin) for running code

---

## Contributing and Feedback

Found an outdated link? Discover a new resource? Have feedback about these materials?

- Check the seminar repository README for contribution guidelines
- Open an issue on the GitHub repository for broken links or suggestions
- Contact the seminar organizers for significant content updates

Last updated: March 2026
