class CreateHousings < ActiveRecord::Migration
  def self.up
    create_table :housings do |t|
      # t.column :name, :string
    end
  end

  def self.down
    drop_table :housings
  end
end
