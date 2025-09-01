import random
from datetime import datetime

class ValidationService:
    def __init__(self):
        self.validation_rules = [
            {
                'name': 'IFC Schema Validation',
                'description': 'Validates IFC file structure and syntax',
                'category': 'Schema',
                'severity': 'critical'
            },
            {
                'name': 'Property Completeness',
                'description': 'Checks for required property sets',
                'category': 'Properties',
                'severity': 'warning'
            },
            {
                'name': 'Clash Detection',
                'description': 'Identifies geometric interferences',
                'category': 'Geometry',
                'severity': 'critical'
            },
            {
                'name': 'Data Integrity',
                'description': 'Verifies data consistency and validity',
                'category': 'Data',
                'severity': 'warning'
            },
            {
                'name': 'Naming Convention',
                'description': 'Checks compliance with naming standards',
                'category': 'Standards',
                'severity': 'info'
            },
            {
                'name': 'Material Assignment',
                'description': 'Validates material data completeness',
                'category': 'Materials',
                'severity': 'warning'
            },
            {
                'name': 'Spatial Structure',
                'description': 'Verifies building hierarchy',
                'category': 'Structure',
                'severity': 'critical'
            },
            {
                'name': 'Units Consistency',
                'description': 'Checks for consistent unit usage',
                'category': 'Standards',
                'severity': 'warning'
            }
        ]

    def validate_model(self, ifc_results):
        """Run all validation rules on the processed IFC model"""
        if not ifc_results:
            return []

        validation_results = []

        for rule in self.validation_rules:
            result = self._run_validation_rule(rule, ifc_results)
            validation_results.append(result)

        return validation_results

    def _run_validation_rule(self, rule, ifc_results):
        """Run a specific validation rule"""
        # Mock validation logic for demo
        rule_name = rule['name']

        if rule_name == 'IFC Schema Validation':
            status = 'passed' if ifc_results.get('schema_valid', True) else 'critical'
            issues = 0 if status == 'passed' else random.randint(1, 5)

        elif rule_name == 'Property Completeness':
            coverage = random.uniform(0.7, 0.95)
            if coverage > 0.9:
                status = 'passed'
                issues = 0
            elif coverage > 0.8:
                status = 'warning'
                issues = random.randint(10, 50)
            else:
                status = 'critical'
                issues = random.randint(50, 100)

        elif rule_name == 'Clash Detection':
            # Simulate clash detection based on model complexity
            total_elements = ifc_results.get('total_elements', 0)
            clash_probability = min(0.3, total_elements / 10000)  # More elements = higher chance

            if random.random() > clash_probability:
                status = 'passed'
                issues = 0
            else:
                status = 'critical'
                issues = random.randint(1, min(20, total_elements // 100))

        elif rule_name == 'Data Integrity':
            status = random.choices(['passed', 'warning'], weights=[0.8, 0.2])[0]
            issues = 0 if status == 'passed' else random.randint(1, 10)

        else:
            # Default logic for other rules
            status = random.choices(['passed', 'warning', 'critical'], weights=[0.6, 0.3, 0.1])[0]
            if status == 'passed':
                issues = 0
            elif status == 'warning':
                issues = random.randint(5, 30)
            else:
                issues = random.randint(10, 50)

        return {
            'name': rule_name,
            'description': rule['description'],
            'category': rule['category'],
            'severity': rule['severity'],
            'status': status,
            'issues': issues,
            'timestamp': datetime.utcnow().isoformat()
        }

    def get_custom_rules(self):
        """Return available custom validation rules"""
        return [
            {
                'name': 'Fire Rating Requirements',
                'description': 'Validates fire rating properties for safety compliance',
                'enabled': True
            },
            {
                'name': 'Accessibility Standards',
                'description': 'Checks compliance with accessibility requirements',
                'enabled': False
            },
            {
                'name': 'Energy Performance',
                'description': 'Validates energy-related properties and values',
                'enabled': True
            }
        ]

    def run_custom_validation(self, rule_name, ifc_results):
        """Run a custom validation rule"""
        # Mock implementation for custom rules
        return {
            'name': rule_name,
            'status': random.choice(['passed', 'warning', 'critical']),
            'issues': random.randint(0, 20),
            'details': f'Custom validation completed for {rule_name}'
        }
