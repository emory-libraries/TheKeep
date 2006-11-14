class SrcStillImage < ActiveRecord::Base
  belongs_to :content
  belongs_to :form
  belongs_to :housing
  has_many :TechImages
end
