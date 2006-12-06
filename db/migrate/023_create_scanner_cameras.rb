class CreateScannerCameras < ActiveRecord::Migration
  def self.up
    create_table :scanner_cameras do |t|
      # t.column :name, :string
    end
  end

  def self.down
    drop_table :scanner_cameras
  end
end
