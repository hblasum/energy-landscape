import yaml
import sqlite3

# Connect to the database
conn = sqlite3.connect('landscape.db')

# Create a cursor object
cursor = conn.cursor()

def create_tables():
  """
  Creates tables in the database for categories, subcategories, and items.
  """
  cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                      name text PRIMARY KEY
                  )''')
  cursor.execute('''CREATE TABLE IF NOT EXISTS subcategories (
                      name text PRIMARY KEY,
                      category text,
                      FOREIGN KEY (category) REFERENCES categories(name)
                  )''')
  cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                      name text PRIMARY KEY,
                      subcategory text,
                      description text,
                      homepage_url text,
                      repo_url text,
                      logo text,
                      crunchbase text,
                      extra text,
                      category text,
                      FOREIGN KEY (subcategory) REFERENCES subcategories(name)
                  )''')

def insert_data(data):
  """
  Inserts data from the YAML file into the database tables.
  """
  for category in data['landscape']:
    category_name = category['name']
    cursor.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (category_name,))
    for subcategory in category['subcategories']:
      subcategory_name = subcategory['name']
      subcategory_category = category_name
      cursor.execute('INSERT OR IGNORE INTO subcategories (name, category) VALUES (?, ?)', (subcategory_name, subcategory_category))
      for item in subcategory['items']:
        item_name = item['name']
        item_subcategory = subcategory_name
        item_description = item.get('description')
        item_homepage_url = item.get('homepage_url')
        item_repo_url = item.get('repo_url')
        item_logo = item.get('logo')
        item_crunchbase = item.get('crunchbase')
        item_extra = item.get('extra')
        cursor.execute('''INSERT OR IGNORE INTO items (name, subcategory, description, homepage_url, repo_url, logo, crunchbase, extra, category) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (item_name, item_subcategory, item_description, item_homepage_url, item_repo_url, item_logo, item_crunchbase, str(item_extra), category_name))

def main():
  # Open the YAML file
  with open('landscape.yaml', 'r') as f:
    data = yaml.safe_load(f)

  # Create tables in the database
  create_tables()

  # Insert data into the database tables
  insert_data(data)

  # Commit the changes to the database
  conn.commit()

if __name__ == '__main__':
  main()