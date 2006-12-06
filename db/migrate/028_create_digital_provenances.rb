class CreateDigitalProvenances < ActiveRecord::Migration
  def self.up
    create_table :digital_provenances do |t|
      # t.column :name, :string
    end
  end

  def self.down
    drop_table :digital_provenances
  end
end
