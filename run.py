import os
from PIL import Image
import re
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
from app.models import solve_optimization_problem

# environment variables
load_dotenv()

# Google Generative AI API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from the Gemini model
def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

# Fonction extraction image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("Aucune image trouvée")

# fonction pour extraire la réponse manuellement
def parse_response(response):
    response_dict = {}
    
    # Extract the objective function
    obj_match = re.search(r'Max\s+([\d\w\s\+\-]+)', response)
    if obj_match:
        objective_str = obj_match.group(1).strip()
        terms = re.findall(r'(\d+)([a-zA-Z]+)', objective_str)
        response_dict['objective'] = {term[1]: int(term[0]) for term in terms}
    
    # Debug: print the objective function
    print("Debug - Objective Function")
    print(response_dict['objective'])

    # Extract constraints
    constraints = {}
    constraint_matches = re.findall(r'([\d\w\s\+\-]+)\s*(<=|>=)\s*(\d+)', response)
    for i, cstr in enumerate(constraint_matches):
        lhs, operator, rhs = cstr
        terms = re.findall(r'(\d*)([a-zA-Z]+)', lhs)
        constraint = {term[1]: int(term[0] if term[0] else 1) for term in terms}
        constraint['rhs'] = int(rhs)
        constraint['operator'] = operator  # Save the operator for further use
        constraints[f'constraint-{i+1}'] = constraint
    
    # Debug: print the extracted constraints
    print("Debug - Constraints")
    for name, constraint in constraints.items():
        print(f"{name}: {constraint}")

    response_dict.update(constraints)
    return response_dict



# Streamlit page
st.set_page_config(page_title="Gemini Image DEMO")
st.header("Gemini application")

input_text = """
    Solve this problem by following the instructions below:
    - Put on the first line the objective function
    example:
        Max ax + by + c 
    - Put next the constraints functions
    example: 
        Constraints: 
            inequalities systems
"""

uploaded_file = st.file_uploader("Choisi une image...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)    

submit = st.button("Solve the problem")

input_prompt1 = """
    You are an expert in solving operational research problems. Please give the 
    mathematics equation to solve the problem in the picture. Don't tell anything else
    apart from the mathematics equation, don't give any solution.
    Your output must be:
        first: always a maximization objective function, and if the problem is a minimization
        case, do the necessary transformation to change it into a maximization objective function.
        second: All the constraints must be less than or equal constraints, and if it is a greater than or
        equal constraint, do the necessary transformation to change it into less than or equal except the 
        positivity constraint.
        """

if submit:
    image_data = input_image_setup(uploaded_file)
    response1 = get_gemini_response(input_text, image_data, input_prompt1)
    
    st.subheader("La réponse est: ")
    st.write(f"{response1}")

    # Debug
    print("Debug - Raw Response")
    print(response1)
    
    # Extraction des réponses
    try:
        response_dict = parse_response(response1)
        print("Reponse extrait:")
        print(response_dict)
        
        if "objective" not in response_dict:
            st.error("Il manque la fonction objective.")
        if not any(k.startswith("constraint") for k in response_dict):
            st.error("Il manque les contraintes.")
        
        objective = response_dict.get("objective", {})
        constraints = {k: v for k, v in response_dict.items() if k.startswith("constraint")}

        if objective and constraints:
            # Transform constraints with >= to <=
            transformed_constraints = {}
            for name, constraint in constraints.items():
                if constraint.get('operator') == '>=':
                    transformed_constraint = {k: -v for k, v in constraint.items() if k not in ['operator', 'rhs']}
                    transformed_constraint['rhs'] = -constraint['rhs']
                    transformed_constraints[name] = transformed_constraint
                else:
                    transformed_constraints[name] = {k: v for k, v in constraint.items() if k != 'operator'}

            # Solve with Pyomo
            results = solve_optimization_problem(objective, transformed_constraints)

            # Display results in Streamlit
            st.subheader("Résultats optimaux:")
            for var, value in results["variables"].items():
                st.write(f"Valeur optimale de {var}: {value}")
            st.write(f"Valeur optimale de la fonction objective: {results['objective_value']}")

        else:
            st.error("Il manque des éléments.")
    except Exception as e:
        st.error(f"Erreur d'extraction des réponses : {str(e)}")



    
