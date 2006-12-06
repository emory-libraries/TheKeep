class CreateSrcSounds < ActiveRecord::Migration
  def self.up
    create_table :src_sounds do |t|
      # t.column :name, :string
    end
  end

  def self.down
    drop_table :src_sounds
  end
end
