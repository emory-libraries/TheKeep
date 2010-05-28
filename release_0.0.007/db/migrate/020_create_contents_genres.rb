class CreateContentsGenres < ActiveRecord::Migration
  def self.up
    create_table :contents_genres do |t|
      # t.column :name, :string
    end
  end

  def self.down
    drop_table :contents_genres
  end
end
