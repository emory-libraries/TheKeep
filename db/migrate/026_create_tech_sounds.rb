class CreateTechSounds < ActiveRecord::Migration
  def self.up
    create_table :tech_sounds do |t|
      # t.column :name, :string
    end
  end

  def self.down
    drop_table :tech_sounds
  end
end
