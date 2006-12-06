class CreateTechImages < ActiveRecord::Migration
  def self.up
    create_table :tech_images do |t|
      # t.column :name, :string
    end
  end

  def self.down
    drop_table :tech_images
  end
end
