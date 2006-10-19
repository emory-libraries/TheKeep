class CreateAccessRights < ActiveRecord::Migration
  def self.up
    create_table :access_rights do |t|
      # t.column :name, :string
    end
  end

  def self.down
    drop_table :access_rights
  end
end
