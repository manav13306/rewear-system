# ReWear Clothing System - Sustainability Calculations
# Environmental impact calculation utilities

from config import Config

class SustainabilityCalculator:
    """
    Calculates environmental impact of clothing reuse activities
    """
    
    # Constants (from Config)
    CO2_PER_ITEM_KG = Config.CO2_PER_ITEM_KG  # kg CO2
    WATER_PER_ITEM_LITERS = Config.WATER_PER_ITEM_LITERS  # liters
    TEXTILE_WASTE_PER_ITEM_KG = Config.TEXTILE_WASTE_PER_ITEM_KG  # kg
    
    @staticmethod
    def calculate_co2_reduction(rewear_count):
        """
        Calculate CO2 reduction from rewearing items
        
        Args:
            rewear_count: Number of times item was reworn
            
        Returns:
            CO2 reduction in kg
        """
        return rewear_count * SustainabilityCalculator.CO2_PER_ITEM_KG
    
    @staticmethod
    def calculate_water_saved(items_rented_or_exchanged):
        """
        Calculate water saved from renting/exchanging instead of buying new
        
        Args:
            items_rented_or_exchanged: Number of items rented or exchanged
            
        Returns:
            Water saved in liters
        """
        return items_rented_or_exchanged * SustainabilityCalculator.WATER_PER_ITEM_LITERS
    
    @staticmethod
    def calculate_textile_waste_prevented(items_count):
        """
        Calculate textile waste prevented
        
        Args:
            items_count: Number of items prevented from landfill
            
        Returns:
            Textile waste prevented in kg
        """
        return items_count * SustainabilityCalculator.TEXTILE_WASTE_PER_ITEM_KG
    
    @staticmethod
    def calculate_environmental_impact_score(co2_saved, water_saved, textile_prevented):
        """
        Calculate overall environmental impact score
        
        Args:
            co2_saved: CO2 saved in kg
            water_saved: Water saved in liters
            textile_prevented: Textile waste prevented in kg
            
        Returns:
            Impact score (higher is better)
        """
        # Weighted score calculation
        co2_score = (co2_saved / SustainabilityCalculator.CO2_PER_ITEM_KG) * 100
        water_score = (water_saved / SustainabilityCalculator.WATER_PER_ITEM_LITERS) * 100
        textile_score = (textile_prevented / SustainabilityCalculator.TEXTILE_WASTE_PER_ITEM_KG) * 50
        
        # Combined score
        total_score = (co2_score * 0.4) + (water_score * 0.4) + (textile_score * 0.2)
        return round(total_score, 2)
    
    @staticmethod
    def get_eco_equivalent(co2_saved_kg):
        """
        Convert CO2 savings to relatable equivalents
        
        Args:
            co2_saved_kg: CO2 saved in kg
            
        Returns:
            Dictionary with environmental equivalents
        """
        # 1 tree absorbs ~22 kg CO2/year
        trees_equivalent = round(co2_saved_kg / 22, 2)
        
        # Average car produces ~4.6 metric tons CO2/year (12,582 kg per 12,582 miles)
        car_miles_prevented = round((co2_saved_kg / 4.6) * 12582, 2)
        
        # Average flight produces 90 kg CO2 per 1000 miles
        flight_miles = round((co2_saved_kg / 90) * 1000, 2)
        
        return {
            'trees_equivalent': trees_equivalent,
            'car_miles_prevented': car_miles_prevented,
            'flight_miles_prevented': flight_miles,
            'co2_kg': co2_saved_kg
        }
    
    @staticmethod
    def get_water_equivalent(water_saved_liters):
        """
        Convert water savings to relatable equivalents
        
        Args:
            water_saved_liters: Water saved in liters
            
        Returns:
            Dictionary with water equivalents
        """
        # Average shower uses 95 liters
        showers = round(water_saved_liters / 95, 2)
        
        # Olympic pool = 2,500,000 liters
        pools = round(water_saved_liters / 2500000, 4)
        
        return {
            'showers': showers,
            'olympic_pools': pools,
            'liters': water_saved_liters
        }


class ImpactReport:
    """
    Generate sustainability impact reports
    """
    
    @staticmethod
    def get_user_impact_summary(user):
        """
        Get comprehensive impact summary for a user
        
        Args:
            user: User object
            
        Returns:
            Dictionary with impact summary
        """
        calculator = SustainabilityCalculator()
        
        return {
            'user_id': str(user.id),
            'username': user.username,
            'total_items_reworn': user.items_reworn,
            'total_items_rented': user.items_rented,
            'total_items_sold': user.items_sold,
            'total_items_exchanged': user.items_exchanged,
            'carbon_saved_kg': user.carbon_saved_kg,
            'water_saved_liters': user.water_saved_liters,
            'reputation_score': user.reputation_score,
            'co2_equivalents': calculator.get_eco_equivalent(user.carbon_saved_kg),
            'water_equivalents': calculator.get_water_equivalent(user.water_saved_liters),
            'impact_score': calculator.calculate_environmental_impact_score(
                user.carbon_saved_kg,
                user.water_saved_liters,
                user.items_rented + user.items_sold + user.items_reworn + user.items_exchanged
            )
        }
    
    @staticmethod
    def get_global_impact_summary(users, total_items_listed=0):
        """
        Get global environmental impact
        
        Args:
            users: List of user objects
            total_items_listed: Total number of items in system
            
        Returns:
            Dictionary with global impact metrics
        """
        total_co2 = sum(user.carbon_saved_kg for user in users)
        total_water = sum(user.water_saved_liters for user in users)
        total_items = sum(user.items_reworn + user.items_rented + user.items_sold + user.items_exchanged for user in users)
        
        calculator = SustainabilityCalculator()
        
        return {
            'total_users': len(users),
            'total_co2_reduced_kg': total_co2,
            'total_water_saved_liters': total_water,
            'total_items_involved': total_items,
            'total_items_listed': total_items_listed,
            'average_user_impact': {
                'co2_kg': round(total_co2 / len(users), 2) if users else 0,
                'water_liters': round(total_water / len(users), 2) if users else 0
            },
            'co2_equivalents': calculator.get_eco_equivalent(total_co2),
            'water_equivalents': calculator.get_water_equivalent(total_water),
            'global_impact_score': calculator.calculate_environmental_impact_score(
                total_co2, total_water, total_items
            )
        }
