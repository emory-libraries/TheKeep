class CreateDescriptionDatas < ActiveRecord::Migration
  def self.up
    create_table :description_datas do |t|
      # t.column :name, :string
    end
  end

  def self.down
    drop_table :description_datas
  end
end
