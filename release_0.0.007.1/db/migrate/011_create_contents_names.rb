class CreateContentsNames < ActiveRecord::Migration
  def self.up
    create_table :contents_names do |t|
      # t.column :name, :string
    end
  end

  def self.down
    drop_table :contents_names
  end
end
