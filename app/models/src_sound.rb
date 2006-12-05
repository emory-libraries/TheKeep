class SrcSound < ActiveRecord::Base
  belongs_to :content
  belongs_to :form
  belongs_to :housing
  belongs_to :speed
  belongs_to :TransferEngineer, :class_name => "StaffName", :foreign_key => "transfer_engineer_staff_id"
  has_many   :TechSounds
end
