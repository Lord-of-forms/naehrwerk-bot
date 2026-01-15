#!/usr/bin/env python3
"""
NährWerk Web Dashboard - Ernährungs-Tracking und Analyse
"""
import os
from flask import Flask, render_template, jsonify, request, redirect, url_for
from supabase import create_client, Client
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    """Homepage mit Benutzerübersicht"""
    try:
        # Get all users
        users = supabase.table('users').select('*').execute()
        return render_template('index.html', users=users.data if users.data else [])
    except Exception as e:
        logger.error(f"Error loading users: {e}")
        return render_template('index.html', users=[], error=str(e))

@app.route('/user/<int:user_id>')
def user_dashboard(user_id):
    """Benutzer-Dashboard mit Mahlzeiten und Statistiken"""
    try:
        # Get user info
        user = supabase.table('users').select('*').eq('id', user_id).execute()
        if not user.data:
            return "User not found", 404
        
        # Get meals for the last 7 days
        seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()
        meals = supabase.table('meals').select('*').eq('user_id', user_id).gte('created_at', seven_days_ago).order('created_at', desc=True).execute()
        
        # Get household members
        household = supabase.table('household_members').select('*').eq('user_id', user_id).execute()
        
        # Get shopping lists
        shopping_lists = supabase.table('shopping_lists').select('*, shopping_list_items(*)').eq('user_id', user_id).order('created_at', desc=True).limit(5).execute()
        
        return render_template('user_dashboard.html', 
                             user=user.data[0],
                             meals=meals.data if meals.data else [],
                             household=household.data if household.data else [],
                             shopping_lists=shopping_lists.data if shopping_lists.data else [])
    except Exception as e:
        logger.error(f"Error loading user dashboard: {e}")
        return f"Error: {e}", 500

@app.route('/api/meals')
def api_meals():
    """API Endpoint für Mahlzeiten-Daten"""
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        meals = supabase.table('meals').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(50).execute()
        return jsonify(meals.data if meals.data else [])
    except Exception as e:
        logger.error(f"Error fetching meals: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/shopping-list', methods=['GET', 'POST'])
def api_shopping_list():
    """API Endpoint für Einkaufslisten"""
    if request.method == 'GET':
        try:
            user_id = request.args.get('user_id')
            if not user_id:
                return jsonify({'error': 'user_id required'}), 400
            
            lists = supabase.table('shopping_lists').select('*, shopping_list_items(*)').eq('user_id', user_id).execute()
            return jsonify(lists.data if lists.data else [])
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.json
            result = supabase.table('shopping_lists').insert(data).execute()
            return jsonify(result.data[0] if result.data else {}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
