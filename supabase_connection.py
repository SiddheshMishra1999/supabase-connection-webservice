from supabase import create_client, Client

import os

# Connecting database
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(SUPABASE_URL,  SUPABASE_ANON_KEY)