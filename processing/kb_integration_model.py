import os
import yaml
import PyPDF2
import spacy
from datetime import date
import logging


class KBArticleConverter:
    def __init__(self, pdf_path, log_file="conversion.log"):
        """
        Initialize the converter with a PDF path and logging setup
        
        Args:
            pdf_path (str): Full path to the PDF file
            log_file (str): Path for the log file
        """
        self.pdf_path = pdf_path

        # Set up logging
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger()

        # Load SpaCy NLP model
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            self.logger.info("Downloading SpaCy model...")
            from spacy.cli import download
            download('en_core_web_sm')
            self.nlp = spacy.load('en_core_web_sm')
    
    def extract_pdf_text(self):
        """
        Extract text from PDF file
        
        Returns:
            str: Extracted text from PDF
        """
        with open(self.pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            full_text = ""
            
            for page in reader.pages:
                full_text += page.extract_text() + "\n"
            
            return full_text
    
    def parse_configuration(self, text):
        """
        Parse extracted text into a structured configuration
        
        Args:
            text (str): Extracted text from PDF
        
        Returns:
            dict: Structured configuration
        """
        # Process text with SpaCy
        doc = self.nlp(text)
        
        # Configuration dictionary to populate
        config = {
            'knowledge_base': {
                'source_file': os.path.basename(self.pdf_path),
                'extraction_date': date.today().isoformat()
            },
            'system_info': {},
            'actions': [],
            'dependencies': {},
            'validations': []
        }
        
        # Extract key entities
        entities = {}
        for ent in doc.ents:
            if ent.label_ not in entities:
                entities[ent.label_] = []
            entities[ent.label_].append(ent.text)
        
        # Populate system info
        if 'ORG' in entities:
            config['system_info']['organizations'] = entities['ORG']
        if 'PRODUCT' in entities:
            config['system_info']['products'] = entities['PRODUCT']
        
        # Extract actions using dependency parsing
        actions = []
        for token in doc:
            if token.dep_ in ['ROOT', 'xcomp', 'advcl'] and token.pos_ == 'VERB':
                actions.append({
                    'action': token.lemma_,
                    'context': " ".join([t.text for t in token.subtree])
                })
        config['actions'] = actions
        
        # Basic dependency mapping
        dependency_map = {}
        for token in doc:
            if token.dep_ not in ['punct', 'ROOT']:
                dependency_map[token.text] = {
                    'dependency': token.dep_,
                    'head': token.head.text
                }
        config['dependencies'] = dependency_map
        
        # Extract validation-like statements
        validation_statements = []
        for sent in doc.sents:
            if any(keyword in sent.text.lower() for keyword in ['must', 'should', 'verify', 'check']):
                validation_statements.append(sent.text)
        config['validations'] = validation_statements
        
        return config
    
    def save_to_yaml(self, config, output_path="/Users/nandish.chokshi/Downloads/NLP_Based_KBA/config/KB-2_config.yaml"):
        """
        Save configuration to YAML file
        
        Args:
            config (dict): Configuration dictionary
            output_path (str): Path to save YAML file
        
        Returns:
            str: Path to saved YAML file
        """
        with open(output_path, 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
        
        self.logger.info(f"Configuration saved to {output_path}")
        return output_path
    
    def convert(self):
        """
        Complete conversion process
        
        Returns:
            dict: Extracted configuration
        """
        # Extract text from PDF
        text = self.extract_pdf_text()
        self.logger.info(f"Extracted text from {self.pdf_path}")
        
        # Parse configuration
        config = self.parse_configuration(text)
        self.logger.info(f"Parsed configuration: {len(config['actions'])} actions, {len(config['validations'])} validations")
        
        # Save to YAML
        self.save_to_yaml(config)
        
        return config


def main():
    # Replace with your PDF path
    pdf_path = "/Users/nandish.chokshi/Downloads/NLP_Based_KBA/data/raw/KB-2.pdf"
    
    # Create converter
    converter = KBArticleConverter(pdf_path)
    
    # Convert PDF to configuration
    config = converter.convert()
    
    # Print summary to the terminal
    print(f"Conversion complete! Extracted {len(config['actions'])} actions and {len(config['validations'])} validations.")
    print("Configuration saved")


if __name__ == "__main__":
    main()
