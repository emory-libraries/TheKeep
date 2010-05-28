class CreateRestrictions < ActiveRecord::Migration
  def self.up
    create_table :restrictions do |t|
      # t.column :name, :string
    end
  end

  def self.down
    drop_table :restrictions
  end
end
