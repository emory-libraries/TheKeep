class CreateContentsLanguages < ActiveRecord::Migration
  def self.up
    create_table :contents_languages do |t|
      # t.column :name, :string
    end
  end

  def self.down
    drop_table :contents_languages
  end
end
