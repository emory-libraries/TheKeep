class CreateSrcStillImages < ActiveRecord::Migration
  def self.up
    create_table :src_still_images do |t|
      # t.column :name, :string
    end
  end

  def self.down
    drop_table :src_still_images
  end
end
