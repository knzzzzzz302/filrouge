# Modele de donnees

## Entites
- agencies(id, name, city, region)
- users(id, email, password_hash, role, agency_id)
- clients(id, first_name, last_name, email, phone, budget_min, budget_max)
- properties(id, reference, type, city, price, area_m2, rooms, status, agency_id)
- transactions(id, property_id, buyer_client_id, seller_client_id, amount, status, signed_at)
- property_views(id, property_id, viewed_at, channel)

## Relations
- Une agence possede plusieurs users/properties
- Une transaction est liee a un bien et a des clients
- Les vues de biens alimentent les analyses de popularite
