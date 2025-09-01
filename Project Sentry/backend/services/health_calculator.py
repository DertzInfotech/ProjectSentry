import math

class HealthCalculator:
    def __init__(self):
        self.severity_weights = {
            'critical': 10,
            'warning': 3,
            'info': 1
        }

        self.category_weights = {
            'Schema': 0.25,
            'Geometry': 0.20,
            'Properties': 0.20,
            'Data': 0.15,
            'Standards': 0.10,
            'Materials': 0.10
        }

    def calculate_score(self, validation_results):
        """Calculate overall model health score based on validation results"""
        if not validation_results:
            return {
                'overall_score': 0,
                'category_scores': {},
                'total_issues': 0,
                'critical_issues': 0,
                'warning_issues': 0,
                'info_issues': 0,
                'recommendations': []
            }

        # Count issues by severity
        critical_issues = sum(1 for r in validation_results if r['status'] == 'critical')
        warning_issues = sum(1 for r in validation_results if r['status'] == 'warning')  
        info_issues = sum(1 for r in validation_results if r['status'] == 'info')

        # Calculate weighted penalty
        total_penalty = 0
        max_possible_penalty = 0

        category_penalties = {}

        for result in validation_results:
            category = result.get('category', 'Other')
            status = result['status']
            issues_count = result.get('issues', 0)

            if category not in category_penalties:
                category_penalties[category] = 0

            # Calculate penalty for this rule
            if status == 'critical':
                penalty = min(100, issues_count * self.severity_weights['critical'])
            elif status == 'warning':
                penalty = min(50, issues_count * self.severity_weights['warning'])
            elif status == 'info':
                penalty = min(25, issues_count * self.severity_weights['info'])
            else:
                penalty = 0

            # Apply category weight
            category_weight = self.category_weights.get(category, 0.05)
            weighted_penalty = penalty * category_weight

            category_penalties[category] += penalty
            total_penalty += weighted_penalty
            max_possible_penalty += 100 * category_weight

        # Calculate overall score (0-100)
        overall_score = max(0, min(100, 100 - (total_penalty / max_possible_penalty * 100)))

        # Calculate category scores
        category_scores = {}
        for category, penalty in category_penalties.items():
            category_scores[category] = max(0, 100 - penalty)

        # Generate recommendations
        recommendations = self._generate_recommendations(validation_results, overall_score)

        return {
            'overall_score': round(overall_score, 1),
            'category_scores': category_scores,
            'total_issues': sum([critical_issues, warning_issues, info_issues]),
            'critical_issues': critical_issues,
            'warning_issues': warning_issues,
            'info_issues': info_issues,
            'recommendations': recommendations,
            'health_grade': self._get_health_grade(overall_score)
        }

    def _get_health_grade(self, score):
        """Convert numeric score to letter grade"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'

    def _generate_recommendations(self, validation_results, overall_score):
        """Generate actionable recommendations based on validation results"""
        recommendations = []

        # Check for critical issues
        critical_rules = [r for r in validation_results if r['status'] == 'critical']
        if critical_rules:
            recommendations.append({
                'priority': 'high',
                'title': 'Resolve Critical Issues',
                'description': f'Address {len(critical_rules)} critical validation failures',
                'action': 'Review and fix critical errors in model data and geometry'
            })

        # Check schema issues
        schema_issues = [r for r in validation_results if r['category'] == 'Schema' and r['status'] != 'passed']
        if schema_issues:
            recommendations.append({
                'priority': 'high',
                'title': 'Fix Schema Compliance',
                'description': 'Model does not fully comply with IFC schema',
                'action': 'Review IFC export settings and fix schema violations'
            })

        # Check property completeness
        property_issues = [r for r in validation_results if r['category'] == 'Properties' and r['issues'] > 20]
        if property_issues:
            recommendations.append({
                'priority': 'medium',
                'title': 'Improve Property Completeness',
                'description': 'Many elements are missing required properties',
                'action': 'Add missing property sets to improve data quality'
            })

        # General recommendations based on score
        if overall_score < 60:
            recommendations.append({
                'priority': 'high',
                'title': 'Comprehensive Model Review',
                'description': 'Model health score is below acceptable threshold',
                'action': 'Perform thorough review of all model elements and data'
            })
        elif overall_score < 80:
            recommendations.append({
                'priority': 'medium',
                'title': 'Model Quality Improvements',
                'description': 'Several areas need attention to improve model quality',
                'action': 'Focus on resolving warning-level issues and data gaps'
            })

        return recommendations[:5]  # Return top 5 recommendations
