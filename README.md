# Molecular Discovery Platform

A containerized, microservice-based cheminformatics and machine learning platform for molecular exploration and early-stage drug discovery workflows.

The platform combines RDKit-based molecular analysis, chemical similarity search, chemical space visualization, and machine learning-based solubility prediction behind a unified API Gateway and an interactive Streamlit dashboard.

Status: MVP / actively developed

## Demo



The Streamlit dashboard provides a single interface for:

molecule analysis,
molecular descriptor inspection,
solubility prediction,
similarity search,
nearest-neighbour exploration,
PCA-based chemical space visualization.

## Overview

The goal of this project is to build an extensible molecular discovery platform that connects cheminformatics, machine learning, and production-oriented software engineering.

A user provides a molecule represented as a SMILES string, and the platform can currently:

calculate molecular descriptors,
canonicalize SMILES,
compare two molecular structures,
search for structurally similar compounds,
explore a molecular chemical space,
predict aqueous solubility using a trained ML model,
visualize results through an interactive web dashboard.

The system is designed as a set of independent containerized services communicating through REST APIs.


## Project Goal

The long-term goal is to develop the project into an extensible experimentation and inference platform for computational drug discovery.
