class CreateStaffNames < ActiveRecord::Migration
  def self.up
    create_table :staff_names do |t|
      # t.column :name, :string
    end
  end

  def self.down
    drop_table :staff_names
  end
end
