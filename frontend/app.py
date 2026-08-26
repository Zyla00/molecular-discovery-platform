import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
import streamlit.components.v1 as components

from api_client import client


st.set_page_config(
    page_title="Molecular Discovery Platform",
    page_icon="🧬",
    layout="wide",
)


st.title("Molecular Discovery Platform")

st.caption(
    "Cheminformatics and machine learning platform "
    "for molecular exploration."
)


default_smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"

smiles = st.text_input(
    "SMILES",
    value=default_smiles,
    help="Enter a molecule represented as a SMILES string.",
)

top_k = st.slider(
    "Number of similar compounds",
    min_value=1,
    max_value=20,
    value=5,
)

analyze_button = st.button(
    "Analyze molecule",
    type="primary",
)

if analyze_button:
    try:
        with st.spinner("Analyzing molecule..."):
            analysis = client.analyze_molecule(
                smiles
            )

            depiction = client.molecule_depiction(
                smiles
            )

            drug_likeness = client.drug_likeness(
                smiles
            )

            similarity = client.similarity_search(
                smiles,
                top_k,
            )

            chemical_space = client.chemical_space(
                smiles,
                top_k,
            )

    except requests.HTTPError as exc:
        st.error(
            f"API returned an error: {exc}"
        )
        st.stop()

    except requests.RequestException as exc:
        st.error(
            f"Could not connect to API Gateway: {exc}"
        )
        st.stop()


    st.subheader("Molecule overview")

    molecule = analysis["molecule"]
    descriptors = analysis["descriptors"]

    structure_col, info_col = st.columns(
        [1, 2]
    )

    with structure_col:
        st.markdown("#### 2D structure")

        components.html(
            depiction["svg"],
            height=320,
        )

    with info_col:
        st.markdown("#### Canonical SMILES")

        st.code(
            molecule["canonical_smiles"],
            language=None,
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Molecular Weight",
            f"{descriptors['molecular_weight']:.2f}",
        )

        col2.metric(
            "LogP",
            f"{descriptors['logp']:.2f}",
        )

        col3.metric(
            "TPSA",
            f"{descriptors['tpsa']:.2f}",
        )

        col4, col5, col6 = st.columns(3)

        col4.metric(
            "H-Bond Donors",
            descriptors["h_bond_donors"],
        )

        col5.metric(
            "H-Bond Acceptors",
            descriptors["h_bond_acceptors"],
        )

        col6.metric(
            "Rotatable Bonds",
            descriptors["rotatable_bonds"],
        )

    st.subheader("Drug-likeness")

    lipinski = drug_likeness["lipinski"]
    rules = lipinski["rules"]

    status_col, qed_col, violations_col = st.columns(3)

    status_col.metric(
        "Lipinski Rule of Five",
        (
            "PASS"
            if lipinski["passes_rule_of_five"]
            else "FAIL"
        ),
    )

    qed_col.metric(
        "QED",
        f"{drug_likeness['qed']:.3f}",
    )

    violations_col.metric(
        "Lipinski violations",
        lipinski["violations"],
    )

    st.markdown("#### Lipinski criteria")

    for name, rule in rules.items():
        label = (
            name
            .replace("_", " ")
            .title()
        )

        icon = (
            "✅"
            if rule["passes"]
            else "❌"
        )

        st.write(
            f"{icon} **{label}**: "
            f"{rule['value']:.2f} "
            f"({rule['threshold']})"
        )

    st.subheader("ML predictions")

    solubility = (
        analysis["predictions"]["solubility"]
    )

    prediction_col, model_col = st.columns(2)

    prediction_col.metric(
        "Predicted logS",
        f"{solubility['predicted_log_s']:.3f}",
    )

    model_col.metric(
        "Model",
        solubility["model"],
    )

    st.subheader("Structurally similar compounds")

    similarity_df = pd.DataFrame(
        similarity["results"]
    )

    st.dataframe(
        similarity_df[
            [
                "compound_id",
                "smiles",
                "similarity",
                "measured_log_s",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )


    st.subheader("Chemical space")

    points_df = pd.DataFrame(
        chemical_space["points"]
    )

    points_df["category"] = (
        points_df["is_neighbor"].map(
            {
                True: "Nearest neighbour",
                False: "Compound library",
            }
        )
    )

    fig = px.scatter(
        points_df,
        x="x",
        y="y",
        color="category",
        hover_name="compound_id",
        hover_data={
            "smiles": True,
            "similarity": True,
            "x": False,
            "y": False,
            "category": False,
        },
        labels={
            "x": "PC1",
            "y": "PC2",
        },
        title="PCA projection of Morgan fingerprints",
    )


    # Make background compounds smaller
    # and neighbours easier to identify.

    for trace in fig.data:
        if trace.name == "Compound library":
            trace.update(
                marker={
                    "size": 5,
                    "opacity": 0.45,
                }
            )

        elif trace.name == "Nearest neighbour":
            trace.update(
                marker={
                    "size": 11,
                    "opacity": 1.0,
                }
            )


    query = chemical_space["query"]

    fig.add_trace(
        go.Scatter(
            x=[query["x"]],
            y=[query["y"]],
            mode="markers",
            name="Query molecule",
            marker={
                "size": 22,
                "symbol": "star",
            },
            text=[
                query["smiles"]
            ],
            hovertemplate=(
                "<b>Query molecule</b><br>"
                "SMILES: %{text}<br>"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        height=650,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    explained_variance = (
        chemical_space["explained_variance"]
    )

    st.caption(
        "PCA explained variance: "
        f"PC1 = {explained_variance[0]:.2%}, "
        f"PC2 = {explained_variance[1]:.2%}"
    )

    st.caption(
        "Morgan fingerprints are projected into 2D using PCA. "
        "Nearest neighbours are selected independently using "
        "Tanimoto similarity."
    )