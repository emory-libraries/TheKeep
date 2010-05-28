class CreateAuthorities < ActiveRecord::Migration
  def self.up
    create_table :authorities do |t|
      # t.column :name, :string
    end
  end

  def self.down
    drop_table :authorities
  end
end
