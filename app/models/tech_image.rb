class TechImage < ActiveRecord::Base
  belongs_to :SrcStillImage
  belongs_to :ScannerCamera
  belongs_to :Target
end
